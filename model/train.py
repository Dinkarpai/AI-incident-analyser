import sys
import os
import json
import joblib
import pandas as pd

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, f1_score
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import OneHotEncoder
from sklearn.linear_model import LogisticRegression

from app.preprocessing import clean_text


def train_text_only_model(df, target_col, output_path, model_name):
    X = df[["clean_log_text"]]
    y = df[target_col]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    preprocessor = ColumnTransformer(
        transformers=[
            ("text", TfidfVectorizer(ngram_range=(1, 2)), "clean_log_text"),
        ]
    )

    pipeline = Pipeline([
        ("preprocessor", preprocessor),
        ("clf", LogisticRegression(max_iter=3000, class_weight="balanced"))
    ])

    pipeline.fit(X_train, y_train)
    preds = pipeline.predict(X_test)
    score = f1_score(y_test, preds, average="weighted", zero_division=0)

    print(f"\n{model_name} Report")
    print(classification_report(y_test, preds, zero_division=0))
    print(f"{model_name} weighted F1: {score:.4f}")

    joblib.dump(pipeline, output_path)
    return score


def train_severity_model(df, output_path):
    feature_cols = [
        "clean_log_text",
        "user_count",
        "affected_services_count",
        "service_scope",
        "impact_scope",
    ]

    X = df[feature_cols]
    y = df["severity"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    preprocessor = ColumnTransformer(
        transformers=[
            ("text", TfidfVectorizer(ngram_range=(1, 2)), "clean_log_text"),
            ("cat", OneHotEncoder(handle_unknown="ignore"), ["service_scope", "impact_scope"]),
            ("num", "passthrough", ["user_count", "affected_services_count"]),
        ]
    )

    pipeline = Pipeline([
        ("preprocessor", preprocessor),
        ("clf", LogisticRegression(max_iter=3000, class_weight="balanced"))
    ])

    pipeline.fit(X_train, y_train)
    preds = pipeline.predict(X_test)
    score = f1_score(y_test, preds, average="weighted", zero_division=0)

    print("\nSeverity Report")
    print(classification_report(y_test, preds, zero_division=0))
    print(f"Severity weighted F1: {score:.4f}")

    joblib.dump(pipeline, output_path)
    return score


def main():
    df = pd.read_csv("data/raw/incidents.csv")

    required_cols = [
        "log_text",
        "category",
        "severity",
        "impact_scope",
        "user_count",
        "affected_services_count",
        "service_scope",
        "resolution",
    ]

    df = df.dropna(subset=required_cols).copy()

    df["clean_log_text"] = df["log_text"].apply(clean_text)
    df["user_count"] = pd.to_numeric(df["user_count"], errors="coerce")
    df["affected_services_count"] = pd.to_numeric(df["affected_services_count"], errors="coerce")
    df = df.dropna(subset=["user_count", "affected_services_count"]).copy()

    category_score = train_text_only_model(
        df=df,
        target_col="category",
        output_path="model/incident_model.pkl",
        model_name="Category"
    )

    severity_score = train_severity_model(
        df=df,
        output_path="model/severity_model.pkl"
    )

    impact_scope_score = train_text_only_model(
        df=df,
        target_col="impact_scope",
        output_path="model/impact_scope_model.pkl",
        model_name="Impact Scope"
    )

    metadata = {
        "category_model": "logistic_regression_balanced",
        "severity_model": "logistic_regression_balanced_text_plus_structured_features",
        "impact_scope_model": "logistic_regression_balanced",
        "category_weighted_f1": category_score,
        "severity_weighted_f1": severity_score,
        "impact_scope_weighted_f1": impact_scope_score,
    }

    with open("model/best_models.json", "w") as f:
        json.dump(metadata, f, indent=2)

    print("\nModels saved successfully.")
    print(json.dumps(metadata, indent=2))


if __name__ == "__main__":
    main()

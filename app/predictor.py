import joblib
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from app.preprocessing import clean_text

incident_model = joblib.load("model/incident_model.pkl")
severity_model = joblib.load("model/severity_model.pkl")
impact_scope_model = joblib.load("model/impact_scope_model.pkl")

df = pd.read_csv("data/raw/incidents.csv").copy()
df["clean_log_text"] = df["log_text"].apply(clean_text)


def get_confidence(model, input_df):
    if hasattr(model, "predict_proba"):
        probs = model.predict_proba(input_df)[0]
        return float(max(probs))
    return None


def infer_user_count(impact_scope: str) -> int:
    mapping = {
        "Single User": 1,
        "Multiple Users": 10,
        "Department Wide": 50,
        "System Wide": 300,
    }
    return mapping.get(impact_scope, 1)


def infer_service_scope_and_count(log_text: str):
    text = log_text.lower()

    core_platform_terms = [
        "sso outage",
        "identity provider",
        "idp",
        "company wide",
        "organization wide",
        "all systems",
        "all applications",
        "core platform",
        "central platform",
        "authentication outage",
        "login platform unavailable",
    ]

    if any(term in text for term in core_platform_terms):
        return "Core Platform", 4

    service_keywords = [
        "payroll",
        "hr",
        "vpn",
        "mail",
        "email",
        "teams",
        "calendar",
        "crm",
        "erp",
        "portal",
        "database",
        "reporting",
        "dashboard",
        "application",
        "applications",
        "app",
        "apps",
        "service",
        "services",
        "server",
        "servers",
        "finance",
        "billing",
        "workflow",
    ]

    matched_services = set()
    for keyword in service_keywords:
        if keyword in text:
            matched_services.add(keyword)

    count = len(matched_services)

    if count >= 2:
        return "Multiple Services", count

    if count == 1:
        return "Single Service", 1

    return "Single Service", 1


def apply_category_guardrail(predicted_category, log_text):
    text = log_text.lower()

    auth_keywords = [
        "sso outage",
        "authentication failure",
        "login failed",
        "cannot login",
        "unable to login",
        "mfa failure",
        "sign in failure",
        "sign-in failure",
        "idp",
        "identity provider",
        "login outage",
        "authentication outage",
    ]

    if any(keyword in text for keyword in auth_keywords):
        return "Authentication"

    return predicted_category


def apply_severity_guardrails(predicted_severity, impact_scope, service_scope, user_count, affected_services_count):
    severity_rank = {
        "Low": 1,
        "Medium": 2,
        "High": 3,
        "Critical": 4,
    }

    minimum_severity = predicted_severity

    if impact_scope == "System Wide":
        minimum_severity = "Critical"
    elif service_scope == "Core Platform" and user_count >= 10:
        minimum_severity = "High"
    elif impact_scope == "Department Wide" and affected_services_count >= 2:
        minimum_severity = "High"
    elif impact_scope == "Multiple Users" and affected_services_count >= 2:
        minimum_severity = "High"

    if severity_rank[minimum_severity] > severity_rank[predicted_severity]:
        return minimum_severity

    return predicted_severity


def get_priority(severity, impact_scope):
    if severity == "Critical":
        return "P1"
    if severity == "High" and impact_scope in ["System Wide", "Department Wide"]:
        return "P1"
    if severity == "High":
        return "P2"
    if severity == "Medium":
        return "P3"
    return "P4"


def get_similarity_based_match(log_text, predicted_category=None, predicted_impact_scope=None):
    clean_input = clean_text(log_text)

    candidate_df = df.copy()

    if predicted_category is not None:
        same_category = candidate_df[candidate_df["category"] == predicted_category]
        if not same_category.empty:
            candidate_df = same_category

    if predicted_impact_scope is not None:
        same_scope = candidate_df[candidate_df["impact_scope"] == predicted_impact_scope]
        if not same_scope.empty:
            candidate_df = same_scope

    vectorizer = TfidfVectorizer(ngram_range=(1, 2))
    corpus = candidate_df["clean_log_text"].tolist() + [clean_input]
    tfidf_matrix = vectorizer.fit_transform(corpus)

    input_vector = tfidf_matrix[-1]
    dataset_vectors = tfidf_matrix[:-1]

    similarities = cosine_similarity(input_vector, dataset_vectors).flatten()
    best_idx = similarities.argmax()

    best_row = candidate_df.iloc[best_idx]
    best_score = float(similarities[best_idx])

    return {
        "matched_log_text": best_row["log_text"],
        "matched_category": best_row["category"],
        "matched_impact_scope": best_row["impact_scope"],
        "matched_severity": best_row["severity"],
        "matched_service_scope": best_row["service_scope"],
        "matched_user_count": int(best_row["user_count"]),
        "matched_affected_services_count": int(best_row["affected_services_count"]),
        "matched_resolution": best_row["resolution"],
        "similarity_score": round(best_score, 2),
    }


def predict_log(log_text: str):
    clean = clean_text(log_text)

    category_input = pd.DataFrame([{"clean_log_text": clean}])
    predicted_category_raw = incident_model.predict(category_input)[0]
    predicted_category = apply_category_guardrail(predicted_category_raw, log_text)
    category_confidence = get_confidence(incident_model, category_input)

    impact_input = pd.DataFrame([{"clean_log_text": clean}])
    predicted_impact_scope = impact_scope_model.predict(impact_input)[0]
    impact_scope_confidence = get_confidence(impact_scope_model, impact_input)

    user_count = infer_user_count(predicted_impact_scope)
    service_scope, affected_services_count = infer_service_scope_and_count(log_text)

    severity_input = pd.DataFrame([{
        "clean_log_text": clean,
        "user_count": user_count,
        "affected_services_count": affected_services_count,
        "service_scope": service_scope,
        "impact_scope": predicted_impact_scope,
    }])

    predicted_severity_raw = severity_model.predict(severity_input)[0]
    severity_confidence = get_confidence(severity_model, severity_input)

    final_severity = apply_severity_guardrails(
        predicted_severity=predicted_severity_raw,
        impact_scope=predicted_impact_scope,
        service_scope=service_scope,
        user_count=user_count,
        affected_services_count=affected_services_count,
    )

    priority = get_priority(final_severity, predicted_impact_scope)

    similar_match = get_similarity_based_match(
        log_text=log_text,
        predicted_category=predicted_category,
        predicted_impact_scope=predicted_impact_scope,
    )

    return {
        "log_text": log_text,
        "predicted_category": predicted_category,
        "category_confidence": round(category_confidence, 2) if category_confidence is not None else None,
        "predicted_impact_scope": predicted_impact_scope,
        "impact_scope_confidence": round(impact_scope_confidence, 2) if impact_scope_confidence is not None else None,
        "predicted_severity": final_severity,
        "severity_confidence": round(severity_confidence, 2) if severity_confidence is not None else None,
        "priority": priority,
        "estimated_user_count": user_count,
        "affected_services_count": affected_services_count,
        "service_scope": service_scope,
        "suggested_resolution": similar_match["matched_resolution"],
        "most_similar_incident": {
            "log_text": similar_match["matched_log_text"],
            "category": similar_match["matched_category"],
            "impact_scope": similar_match["matched_impact_scope"],
            "severity": similar_match["matched_severity"],
            "service_scope": similar_match["matched_service_scope"],
            "user_count": similar_match["matched_user_count"],
            "affected_services_count": similar_match["matched_affected_services_count"],
            "similarity_score": similar_match["similarity_score"]
        }
    }

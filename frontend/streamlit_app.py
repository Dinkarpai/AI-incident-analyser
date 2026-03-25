import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="AI Incident Log Analyzer", layout="wide")


def format_confidence(val):
    if val is None:
        return "N/A"
    pct = val * 100
    if val >= 0.7:
        return f"{pct:.1f}% (High)"
    elif val >= 0.4:
        return f"{pct:.1f}% (Medium)"
    return f"{pct:.1f}% (Low)"


def show_severity_badge(severity):
    if severity == "Critical":
        st.error(f"Severity: {severity}")
    elif severity == "High":
        st.warning(f"Severity: {severity}")
    elif severity == "Medium":
        st.info(f"Severity: {severity}")
    else:
        st.success(f"Severity: {severity}")


def show_priority_badge(priority):
    if priority == "P1":
        st.error(f"Priority: {priority}")
    elif priority == "P2":
        st.warning(f"Priority: {priority}")
    elif priority == "P3":
        st.info(f"Priority: {priority}")
    else:
        st.success(f"Priority: {priority}")


st.title("AI Incident Log Analyzer")
st.write("Analyze incident logs, estimate impact, assign priority, and retrieve the closest known incident resolution.")

tab1, tab2 = st.tabs(["Single Log", "CSV Upload"])

with tab1:
    st.subheader("Analyze a Single Incident Log")

    log_text = st.text_area(
        "Enter incident log",
        height=120,
        placeholder="Example: Multiple users cannot access payroll and HR applications after SSO outage"
    )

    if st.button("Analyze"):
        if not log_text.strip():
            st.warning("Please enter a log message.")
        else:
            try:
                res = requests.post(f"{API_URL}/predict", json={"log_text": log_text})

                if res.status_code != 200:
                    st.error(f"API Error: {res.status_code} - {res.text}")
                else:
                    result = res.json()

                    c1, c2, c3, c4 = st.columns(4)

                    with c1:
                        st.metric("Category", result.get("predicted_category", "N/A"))
                        st.metric("Category Confidence", format_confidence(result.get("category_confidence")))

                    with c2:
                        st.metric("Impact Scope", result.get("predicted_impact_scope", "N/A"))
                        st.metric("Impact Confidence", format_confidence(result.get("impact_scope_confidence")))

                    with c3:
                        show_severity_badge(result.get("predicted_severity", "N/A"))
                        st.metric("Severity Confidence", format_confidence(result.get("severity_confidence")))

                    with c4:
                        show_priority_badge(result.get("priority", "N/A"))

                    st.subheader("Impact Details")
                    ic1, ic2, ic3 = st.columns(3)
                    with ic1:
                        st.metric("Estimated User Count", result.get("estimated_user_count", "N/A"))
                    with ic2:
                        st.metric("Affected Services Count", result.get("affected_services_count", "N/A"))
                    with ic3:
                        st.metric("Service Scope", result.get("service_scope", "N/A"))

                    st.subheader("Suggested Resolution")
                    st.success(result.get("suggested_resolution", "No resolution available"))

                    similar = result.get("most_similar_incident")
                    if similar:
                        st.subheader("Most Similar Incident")

                        s1, s2 = st.columns([2, 1])

                        with s1:
                            st.write("**Matched Log**")
                            st.write(similar.get("log_text", "N/A"))

                        with s2:
                            st.metric("Similarity Score", similar.get("similarity_score", "N/A"))

                        sim_df = pd.DataFrame([{
                            "Category": similar.get("category", "N/A"),
                            "Impact Scope": similar.get("impact_scope", "N/A"),
                            "Severity": similar.get("severity", "N/A"),
                            "Service Scope": similar.get("service_scope", "N/A"),
                            "User Count": similar.get("user_count", "N/A"),
                            "Affected Services Count": similar.get("affected_services_count", "N/A"),
                        }])
                        st.dataframe(sim_df, use_container_width=True, hide_index=True)

                    with st.expander("Raw API Response"):
                        st.json(result)

            except Exception as e:
                st.error(f"Could not connect to API: {e}")

with tab2:
    st.subheader("Analyze a CSV File")
    st.caption("Upload a CSV containing a `log_text` column.")

    file = st.file_uploader("Upload CSV", type=["csv"])

    if file is not None:
        try:
            files = {"file": (file.name, file.getvalue(), "text/csv")}
            res = requests.post(f"{API_URL}/upload-csv", files=files)

            if res.status_code != 200:
                st.error(f"API Error: {res.status_code} - {res.text}")
            else:
                data = res.json().get("predictions", [])

                if not data:
                    st.warning("No predictions returned.")
                else:
                    df = pd.DataFrame(data)

                    st.success(f"Analyzed {len(df)} log entries.")

                    st.subheader("Overview")

                    total = len(df)
                    critical = (df["predicted_severity"] == "Critical").sum() if "predicted_severity" in df.columns else 0
                    high = (df["predicted_severity"] == "High").sum() if "predicted_severity" in df.columns else 0
                    p1 = (df["priority"] == "P1").sum() if "priority" in df.columns else 0
                    avg_conf = round(df["severity_confidence"].mean(), 2) if "severity_confidence" in df.columns else 0

                    k1, k2, k3, k4 = st.columns(4)
                    k1.metric("Total Logs", total)
                    k2.metric("Critical", critical)
                    k3.metric("High", high)
                    k4.metric("P1 Incidents", p1)

                    st.metric("Avg Severity Confidence", f"{avg_conf*100:.0f}%")

                    st.dataframe(df, use_container_width=True)

                    csv_data = df.to_csv(index=False).encode("utf-8")
                    st.download_button(
                        "Download Results CSV",
                        data=csv_data,
                        file_name="incident_predictions.csv",
                        mime="text/csv"
                    )

                    st.subheader("Charts")
                    col1, col2, col3 = st.columns(3)

                    with col1:
                        if "predicted_category" in df.columns:
                            fig, ax = plt.subplots(figsize=(4, 3))
                            df["predicted_category"].value_counts().plot(kind="bar", ax=ax)
                            ax.set_title("Category", fontsize=10)
                            ax.set_xlabel("")
                            ax.set_ylabel("")
                            ax.tick_params(axis="x", rotation=30, labelsize=8)
                            ax.tick_params(axis="y", labelsize=8)
                            plt.tight_layout()
                            st.pyplot(fig)

                    with col2:
                        if "predicted_severity" in df.columns:
                            severity_counts = df["predicted_severity"].value_counts()
                            colors = {
                                "Critical": "red",
                                "High": "orange",
                                "Medium": "blue",
                                "Low": "green"
                            }

                            fig, ax = plt.subplots(figsize=(4, 3))
                            severity_counts.plot(
                                kind="bar",
                                ax=ax,
                                color=[colors.get(x, "gray") for x in severity_counts.index]
                            )
                            ax.set_title("Severity", fontsize=10)
                            ax.set_xlabel("")
                            ax.set_ylabel("")
                            ax.tick_params(axis="x", labelsize=8)
                            ax.tick_params(axis="y", labelsize=8)
                            plt.tight_layout()
                            st.pyplot(fig)

                    with col3:
                        if "predicted_impact_scope" in df.columns:
                            fig, ax = plt.subplots(figsize=(4, 3))
                            df["predicted_impact_scope"].value_counts().plot(kind="bar", ax=ax)
                            ax.set_title("Impact Scope", fontsize=10)
                            ax.set_xlabel("")
                            ax.set_ylabel("")
                            ax.tick_params(axis="x", rotation=30, labelsize=8)
                            ax.tick_params(axis="y", labelsize=8)
                            plt.tight_layout()
                            st.pyplot(fig)

        except Exception as e:
            st.error(f"Could not process CSV: {e}")

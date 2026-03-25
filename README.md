# 🚀 AI Incident Log Analyzer

An intelligent system that analyzes IT incident logs, classifies issues, estimates impact, assigns priority (P1–P4), and suggests resolutions using machine learning and similarity-based retrieval.

---

## 🔥 Key Features

- 🧠 **NLP-based classification**
  - Category (Authentication, Infrastructure, Database, etc.)
  - Severity (Low → Critical)
  - Impact Scope (Single User → System Wide)

- ⚡ **Priority Assignment**
  - Automatically assigns P1–P4 based on severity + impact

- 📊 **Impact Estimation**
  - Estimated users affected
  - Number of services impacted
  - Service scope (Single / Multiple / Core Platform)

- 🔍 **Similarity-Based Resolution**
  - Finds closest historical incident
  - Suggests real-world resolution

- 📈 **CSV Batch Analysis**
  - Upload incident logs
  - Get predictions + charts + insights

- 🌐 **Full Stack App**
  - FastAPI backend
  - Streamlit dashboard

---

## 🧠 Tech Stack

- Python
- FastAPI
- Streamlit
- Scikit-learn
- Pandas / NumPy
- Matplotlib

---

## 📊 Example Output

**Input:**

**Output:**
- Category: Authentication  
- Impact: Multiple Users  
- Severity: High  
- Priority: P2  
- Suggested Resolution: Restore SSO service and validate identity provider  

---

## 🚀 How to Run

### 1. Clone the repo
```bash
git clone https://github.com/<your-username>/AI-incident-analyser.git
cd AI-incident-analyser
git clone https://github.com/dinkarpai/AI-incident-analyser.git
cd AI-incident-analyser

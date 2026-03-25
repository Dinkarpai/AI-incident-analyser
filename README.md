# 🚀 AI Incident Log Analyzer

An intelligent system that analyzes IT incident logs, classifies issues, estimates impact, assigns priority (P1–P4), and suggests resolutions using machine learning and similarity-based retrieval.

---

## 🔥 Key Features

<<<<<<< HEAD
- 🧠 NLP-based classification (Category, Severity, Impact Scope)
- ⚡ Priority assignment (P1–P4)
- 📊 Impact estimation (users affected, services impacted)
- 🔍 Similarity-based resolution suggestion
- 📈 CSV batch analysis with charts
- 🌐 FastAPI backend + Streamlit frontend
=======
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
>>>>>>> 4f24aae (Initial commit - AI Incident Log Analyzer)

---

## 🧠 Tech Stack

<<<<<<< HEAD
- Python  
- FastAPI  
- Streamlit  
- Scikit-learn  
- Pandas / NumPy  
- Matplotlib  

---

## 📊 Example

### Input:

Multiple users cannot access payroll and HR applications after SSO outage


### Output:
=======
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
>>>>>>> 4f24aae (Initial commit - AI Incident Log Analyzer)
- Category: Authentication  
- Impact: Multiple Users  
- Severity: High  
- Priority: P2  
- Suggested Resolution: Restore SSO service and validate identity provider  

 HEAD
### Explanation:
The system identifies this as an authentication issue caused by an SSO outage affecting multiple users. Based on impact and severity, it assigns priority P2 and retrieves a similar historical incident to suggest an appropriate resolution.

=======
>>>>>>> 4f24aae (Initial commit - AI Incident Log Analyzer)
---

## 🚀 How to Run

<<<<<<< HEAD
### 1. Clone the repository
```bash
git clone https://github.com/dinkarpai/AI-incident-analyser.git
cd AI-incident-analyser

### 2. Create a virtual enviroment

python -m venv venv
source venv/bin/activate   # Mac/Linux

### 3. Install Dependencies

pip install -r requirements.txt

### 4. Train Models

python model/train.py

### 5. Start Backend (FastAPI)

python -m uvicorn app.main:app --reload

### 6. Run Frontend (Streamlit)

streamlit run frontend/streamlit_app.py


### Project Structure

app/         → FastAPI backend
model/       → Model training & saved models
frontend/    → Streamlit UI
data/        → Incident dataset
=======
### 1. Clone the repo
```bash
git clone https://github.com/<your-username>/AI-incident-analyser.git
cd AI-incident-analyser
git clone https://github.com/dinkarpai/AI-incident-analyser.git
cd AI-incident-analyser
>>>>>>> 4f24aae (Initial commit - AI Incident Log Analyzer)

# 🚀 AI Incident Log Analyzer

An intelligent system that analyzes IT incident logs, classifies issues, estimates impact, assigns priority (P1–P4), and suggests resolutions using machine learning and similarity-based retrieval.

---

## 🔥 Key Features

- 🧠 NLP-based classification (Category, Severity, Impact Scope)
- ⚡ Priority assignment (P1–P4)
- 📊 Impact estimation (users affected, services impacted)
- 🔍 Similarity-based resolution suggestion
- 📈 CSV batch analysis with charts
- 🌐 FastAPI backend + Streamlit frontend

---

## 🧠 Tech Stack

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
- Category: Authentication  
- Impact: Multiple Users  
- Severity: High  
- Priority: P2  
- Suggested Resolution: Restore SSO service and validate identity provider  

### Explanation:
The system identifies this as an authentication issue caused by an SSO outage affecting multiple users. Based on impact and severity, it assigns priority P2 and retrieves a similar historical incident to suggest an appropriate resolution.

---

## 🚀 How to Run

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

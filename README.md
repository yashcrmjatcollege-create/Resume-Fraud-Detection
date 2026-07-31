# 📄 Resume Fraud Detection System

A Flask-based web application that analyzes resumes and detects potential fraudulent or suspicious content using automated techniques.

---

## 🚀 Features

- 📂 Upload resumes (PDF/TXT)
- 🔍 Analyze resume content
- ⚠️ Detect suspicious or fake information
- 🧠 Basic AI-based resume evaluation
- 🗂️ History tracking of analyzed resumes
- 📄 Resume preview (PDF/Text)
- 💾 SQLite database integration

---

## 🏗️ Project Structure

```
resume_fraud_detection/
│── app.py
│── database.py
│── model.py
│── resume_analyzer.py
│── requirements.txt
│── resumes_final.db
│
├── templates/
│   ├── index.html
│   ├── history.html
│   ├── preview_pdf.html
│   ├── preview_text.html
│
├── static/
│   └── style.css
│
├── uploads/
├── resumes/
```

---

## ⚙️ Installation & Setup

### 1. Clone the repository
```bash
git clone https://github.com/your-username/resume-fraud-detection.git
cd resume-fraud-detection
```

### 2. Create virtual environment
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

---

## ▶️ Run the Application

```bash
python app.py
```

Open in browser:
```
http://127.0.0.1:5000/
```

---

## 🧠 How It Works

1. Upload resume  
2. Extract text  
3. Analyze for fraud patterns  
4. Store results  
5. View history  

---

## 📦 Tech Stack

- Python  
- Flask  
- SQLite  
- HTML/CSS  

---

## 🛠️ Future Improvements

- AI/ML model integration  
- Resume scoring  
- User authentication  
- Cloud deployment  

---

## 👨‍💻 Author

**Yash Rajouria**

---

## ⭐ Support

If you like this project, give it a star ⭐ on GitHub!

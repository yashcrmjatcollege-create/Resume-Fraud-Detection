from flask import Flask, render_template, request, redirect
import os
from werkzeug.utils import secure_filename
from resume_analyzer import fraud_score, extract_text
from database import init_db, save_resume, get_history, clear_history
from flask import send_from_directory

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

init_db()

@app.route("/", methods=["GET", "POST"])
def index():
    score = None
    result = None
    reasons = None
    confidence = None
    uploaded_filename = None

    if request.method == "POST":
        file = request.files["resume"]

        if file and file.filename:
            filename = secure_filename(file.filename)
            uploaded_filename = filename

            file_ext = filename.rsplit(".", 1)[-1].lower()
            file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)

            file.save(file_path)

            text = extract_text(file_path, file_ext)
            score, result, reasons, confidence = fraud_score(text)

            save_resume(filename, score, result)

    return render_template(
        "index.html",
        score=score,
        result=result,
        reasons=reasons,
        confidence=confidence,
        uploaded_filename=uploaded_filename
    )
@app.route("/history")
def history():

    data = get_history()

    genuine = sum(1 for r in data if "Genuine" in r[3])
    suspicious = sum(1 for r in data if "Suspicious" in r[3])
    fraud = sum(1 for r in data if "Fraudulent" in r[3])

    return render_template(
        "history.html",
        data=data,
        genuine_count=genuine,
        suspicious_count=suspicious,
        fraud_count=fraud
    )
@app.route("/clear-history")
def clear_all():
    clear_history()
    return redirect("/history")

@app.route("/preview/<filename>")
def preview_resume(filename):
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)

    if not os.path.exists(file_path):
        return "File not found", 404

    file_ext = filename.rsplit(".", 1)[-1].lower()

    # 📄 If PDF → show actual PDF
    if file_ext == "pdf":
        return render_template(
            "preview_pdf.html",
            filename=filename
        )

    # 📄 Otherwise → text preview
    text = extract_text(file_path, file_ext)
    return render_template(
        "preview_text.html",
        filename=filename,
        text=text
    )

@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

if __name__ == "__main__":
    app.run(debug=True)
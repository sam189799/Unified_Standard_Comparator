from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os
from utils.similarity import calculate_similarity, compare_clauses
from config import (
    UPLOAD_FOLDER,
    REPORT_FOLDER,
    SECRET_KEY,
    ALLOWED_EXTENSIONS
)

from utils.pdf_reader import extract_pdf_text
from utils.doc_reader import extract_docx_text
from utils.preprocess import preprocess_text

from utils.similarity import (
    calculate_similarity,
    compare_clauses
)

from utils.clause_extractor import extract_clauses

app = Flask(__name__)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["REPORT_FOLDER"] = REPORT_FOLDER
app.config["SECRET_KEY"] = SECRET_KEY

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(REPORT_FOLDER, exist_ok=True)


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():

    if "file1" not in request.files or "file2" not in request.files:
        return "Please upload both files."

    file1 = request.files["file1"]
    file2 = request.files["file2"]

    if file1.filename == "" or file2.filename == "":
        return "Please select both files."

    if not allowed_file(file1.filename):
        return "Standard 1 must be PDF or DOCX."

    if not allowed_file(file2.filename):
        return "Standard 2 must be PDF or DOCX."

    filename1 = secure_filename(file1.filename)
    filename2 = secure_filename(file2.filename)

    path1 = os.path.join(app.config["UPLOAD_FOLDER"], filename1)
    path2 = os.path.join(app.config["UPLOAD_FOLDER"], filename2)

    file1.save(path1)
    file2.save(path2)

    # Extract text from Document 1
    if filename1.lower().endswith(".pdf"):
        text1 = extract_pdf_text(path1)
    else:
        text1 = extract_docx_text(path1)

    # Extract text from Document 2
    if filename2.lower().endswith(".pdf"):
        text2 = extract_pdf_text(path2)
    else:
        text2 = extract_docx_text(path2)

    # NLP Preprocessing
    processed_text1 = preprocess_text(text1)
    processed_text2 = preprocess_text(text2)

    # Overall Similarity
    similarity_score = calculate_similarity(
        processed_text1,
        processed_text2
    )

    # Clause Extraction
    clauses1 = extract_clauses(text1)
    clauses2 = extract_clauses(text2)

    # Clause Comparison
    comparison = compare_clauses(
        clauses1,
        clauses2
    )

    return render_template(
        "result.html",
        similarity=similarity_score,
        comparison=comparison,
        text1=text1,
        text2=text2
    )


if __name__ == "__main__":
    app.run(debug=True)
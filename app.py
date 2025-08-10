import os
import traceback
from flask import Flask, request, jsonify, render_template
from utils.azure_datalake import upload_file_to_datalake, download_file_from_datalake
from utils.ingestion import extract_text_from_pdf
from utils.vector_store import add_document, search
from utils.chat import generate_response

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file provided"}), 400
        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "Empty filename"}), 400

        filename = file.filename
        upload_file_to_datalake(file.stream, filename)
        file_stream = download_file_from_datalake(filename)

        text, tables = extract_text_from_pdf(file_stream)
        add_document(filename, text)

        return jsonify({"message": f"{filename} uploaded and indexed locally.", "tables": tables})

    except Exception as e:
        app.logger.error("Upload error: %s\n%s", e, traceback.format_exc())
        return jsonify({"error": "Upload failed", "details": str(e)}), 500


@app.route("/ask", methods=["POST"])
def ask():
    try:
        data = request.get_json() or {}
        question = data.get("question", "").strip()
        if not question:
            return jsonify({"error": "No question provided"}), 400

        chunks = search(question, k=5)
        context = " ".join(chunks) if chunks else ""
        answer = generate_response(question, context)

        return jsonify({"answer": answer})

    except Exception as e:
        app.logger.error("Ask error: %s\n%s", e, traceback.format_exc())
        return jsonify({"error": "Ask failed", "details": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)


import pdfplumber
import camelot
import io

def extract_text_from_pdf(file_stream):
    text_content = ""
    tables_data = []

    # Extract text
    with pdfplumber.open(file_stream) as pdf:
        for page in pdf.pages:
            text_content += page.extract_text() + "\n"

    # Reset stream for table extraction
    file_stream.seek(0)
    try:
        tables = camelot.read_pdf(filepath_or_buffer=file_stream, pages='all', flavor='stream')
        for t in tables:
            tables_data.append(t.df.values.tolist())
    except Exception:
        pass

    return text_content, tables_data

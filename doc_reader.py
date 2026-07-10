from docx import Document


def extract_docx_text(docx_path):
    """
    Extract text from a DOCX file.
    """

    document = Document(docx_path)

    text = ""

    for paragraph in document.paragraphs:
        text += paragraph.text + "\n"

    return text
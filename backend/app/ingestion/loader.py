import fitz
from docx import Document
from pathlib import Path

def load_document(file_path):
    path = Path(file_path)
    suffix = path.suffix.lower() 

    if suffix == '.pdf':
        return _load_pdf(file_path)
    elif suffix == '.docx':
        return _load_docx(file_path)
    elif suffix == '.txt':
        return path.read_text(encoding='utf-8')
    else:
        raise ValueError(f'Unsupported file type: {suffix}')

def _load_pdf(file_path):
    doc = fitz.open(file_path)
    return '\n'.join(page.get_text() for page in doc)

def _load_docx(file_path):
    doc = Document(file_path)
    return '\n'.join(p.text for p in doc.paragraphs if p.text.strip())


import pytest
import os
import tempfile
from app.ingestion.loader import load_document
from app.ingestion.chunker import split_text

def test_load_txt():
    with tempfile.NamedTemporaryFile(suffix='.txt', mode='w',
                                     delete=False, encoding='utf-8') as f:
        f.write('Hello world. This is a test document.')
        tmp_path = f.name
    try:
        text = load_document(tmp_path)
        assert 'Hello world' in text
    finally:
        os.unlink(tmp_path)

def test_load_unsupported_format():
    with pytest.raises(ValueError, match='Unsupported file type'):
        load_document('file.xyz')

def test_split_text_basic():
    text = 'word' * 600
    chunks = split_text(text)
    assert len(chunks) > 1

def test_split_text_short():
    text = 'Short text.'
    chunks = split_text(text)
    assert len(chunks) == 1
    assert chunks[0] == 'Short text.'

def test_split_text_overlap():
    text = 'word' * 1000
    chunks = split_text(text)
    assert len(chunks) >= 2
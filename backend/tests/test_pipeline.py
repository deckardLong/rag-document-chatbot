import pytest
from unittest.mock import patch, MagicMock
from app.core.pipeline import run_rag
from app.models.chat import ChatRequest

def make_request(question='What is this?', doc_ids=None):
    return ChatRequest(question=question, document_ids=doc_ids, chat_history=[])

@patch("app.core.pipeline.list_collections")
def test_no_documents_returns_message(mock_list):
    mock_list.return_value = []
    response = run_rag(make_request())
    assert 'No documents' in response.answer
    assert response.sources == []

@patch("app.core.pipeline.generate_answer")
@patch("app.core.pipeline.retrieve_with_scores")
@patch("app.core.pipeline.list_collections")
def test_full_pipeline(mock_list, mock_retrieve, mock_generate):
    mock_list.return_value = ['doc1']
    mock_retrieve.return_value = [
        {'document_id': 'doc1', 'chunk': 'relevant text', 'score': 0.5}
    ]
    mock_generate.return_value = 'The answer is 42.'

    response = run_rag(make_request())
    assert response.answer == 'The answer is 42.'
    assert len(response.sources) == 1
    assert response.sources[0].document_id == 'doc1'

@patch("app.core.pipeline.retrieve")
@patch("app.core.pipeline.retrieve_with_scores")
@patch("app.core.pipeline.list_collections")
def test_fallback_when_threshold_filters_all(mock_list, mock_scored, mock_raw):
    mock_list.return_value = ['doc1']
    mock_scored.return_value = []
    mock_raw.return_value = [
        {'document_id': 'doc1', 'chunk': 'fallback chunk', 'score': 2.0}
    ]
    with patch("app.core.pipeline.generate_answer", return_value="Fallback answer."):
        response = run_rag(make_request())
    assert response.answer == 'Fallback answer.'
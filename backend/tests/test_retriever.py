from unittest.mock import patch, MagicMock
from app.core.retriever import retrieve, retrieve_with_scores

MOCK_RESULTS = [
    {"document_id": "doc1", "chunk": "relevant content here", "score": 0.8},
    {"document_id": "doc1", "chunk": "somewhat related", "score": 1.2},
    {"document_id": "doc2", "chunk": "not very relevant", "score": 1.8},
]

@patch("app.core.retriever.search")
@patch("app.core.retriever.list_collections")
def test_retrieve_uses_all_docs_when_none_given(mock_list, mock_search):
    mock_list.return_value = ['doc1', 'doc2']
    mock_search.return_value = MOCK_RESULTS
    results = retrieve('what is this about?')
    mock_list.assert_called_once()
    assert len(results) == 3

@patch("app.core.retriever.search")
@patch("app.core.retriever.list_collections")
def test_retrieve_with_specific_docs(mock_list, mock_search):
    mock_search.return_value = MOCK_RESULTS[:1]
    results = retrieve('query', document_ids=['doc1'])
    mock_list.assert_not_called()
    assert results[0]['document_id'] =='doc1'

@patch("app.core.retriever.search")
@patch("app.core.retriever.list_collections")
def test_retrieve_empty_when_no_docs(mock_list, mock_search):
    mock_list.return_value = []
    results = retrieve('query')
    mock_search.assert_not_called()
    assert results == []

@patch("app.core.retriever.search")
@patch("app.core.retriever.list_collections")
def test_retrieve_with_scores_filters_threshold(mock_list, mock_search):
    mock_list.return_value = ['doc1']
    mock_search.return_value = MOCK_RESULTS
    results = retrieve_with_scores('query', score_threshold=1.5)
    assert all(r['score'] <= 1.5 for r in results)
    assert len(results) == 2
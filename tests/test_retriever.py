from src.retriever import split_text

def test_split_text_returns_chunks():
    chunks = split_text("one two three four five six", chunk_size=3, overlap=1)
    assert chunks
    assert "one two three" in chunks[0]

def test_empty_text():
    assert split_text("") == []

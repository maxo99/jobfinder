

def test_embedding_client(fix_ollamaembeddingclient):
    try:
        response = fix_ollamaembeddingclient.embed("Test embedding text")
        assert isinstance(response, list), "Embedding response is not a list."
        assert len(response) > 0, "Embedding response is empty."
    except Exception as e:
        fix_ollamaembeddingclient.client.info()
        print("Ollama connection failed:", e)
        raise e




def test_completions(fix_ollamachatclient):
    try:
        response =  fix_ollamachatclient.completions("Test message")
        assert response is not None, "No response from Ollama client."
    except Exception as e:
        fix_ollamachatclient.client.info()
        print("Ollama connection failed:", e)
        raise e


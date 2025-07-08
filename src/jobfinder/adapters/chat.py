from openai import OpenAI
import os
import logging

from openai.types.chat.chat_completion import ChatCompletion

logger = logging.getLogger(__name__)


_client = None
ENABLED = False
if os.environ.get("OPENAI_KEY", ""):
    _client = OpenAI(api_key=os.environ.get("OPENAI_KEY"))
    ENABLED = True


MODEL = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")


def completions(content: str) -> ChatCompletion:
    try:
        if not _client:
            raise Exception("Chat has not been configured")
        logger.info(f"Perfoming completions call with:{MODEL}")
        completion = _client.chat.completions.create(
            model=MODEL,
            response_format={"type": "json_object"},
            messages=[
                {
                    "role": "user",
                    "content": content,
                }
            ],
        )
        logger.info(f"Returned chat completion {completion.id}")
        return completion
    except Exception as e:
        raise e

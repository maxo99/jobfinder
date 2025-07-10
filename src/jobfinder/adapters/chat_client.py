from openai import OpenAI
import os
import logging

from openai.types.chat.chat_completion import ChatCompletion

logger = logging.getLogger(__name__)



class ChatClient:
    def __init__(self):
        self._client = None
        self.ENABLED = False
        if os.environ.get("OPENAI_KEY", ""):
            self._client = OpenAI(api_key=os.environ.get("OPENAI_KEY"))
            self.ENABLED = True
            self.model = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")




    def completions(self,content: str) -> ChatCompletion:
        try:
            if not self._client:
                raise Exception("Chat has not been configured")
            logger.info(f"Perfoming completions call with:{self.model}")
            completion = self._client.chat.completions.create(
                model=self.model,
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

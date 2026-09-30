import asyncio

import ollama


class OllamaClient:

    def __init__(
        self,
        model: str = "llama3.2",
    ):
        self.model = model

    async def generate(
        self,
        prompt: str,
    ) -> str:

        response = await asyncio.to_thread(
            ollama.chat,
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )

        return response["message"]["content"]
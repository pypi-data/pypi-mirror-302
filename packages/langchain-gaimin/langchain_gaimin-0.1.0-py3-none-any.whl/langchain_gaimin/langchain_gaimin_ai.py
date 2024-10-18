import os
from langchain_ollama import OllamaLLM

class LangchainGaiminAI(OllamaLLM):
    def __init__(self, *args, **kwargs):

        base_url = kwargs.get("base_url", os.getenv("GAIMIN_AI_API_URL", "https://api.cloud.gaimin.io"))
        base_path = os.getenv("GAIMIN_AI_API_MODEL_BASE_PATH", "ai/text-2-text")
        base_url = f"{base_url}/{base_path}"

        model = kwargs.get("model", os.getenv("OLLAMA_MODEL", "llama3.2"))
        api_key = os.getenv("GAIMIN_AI_API_TOKEN")

        if not api_key:
            raise ValueError("API key not provided.")

        temperature = kwargs.get("temperature", 0.1)
        keep_alive = kwargs.get("keep_alive", -1)
        name = kwargs.get("name", "GAIMIN AI Decentralized LLM Service")

        client_kwargs = kwargs.get("client_kwargs", {
            "headers": {
                "X-API-KEY": api_key
            }
        })

        super().__init__(
            base_url=base_url,
            model=model,
            temperature=temperature,
            keep_alive=keep_alive,
            name=name,
            client_kwargs=client_kwargs,
            *args,
            **kwargs
        )

import unittest
from langchain_gaimin import LangchainGaiminAI
from langchain_gaimin import LangchainGaiminEmbeddings
from langchain_core.prompts import ChatPromptTemplate
import asyncio

class TestAPIClient(unittest.TestCase):
    def test_llm_invoke_success(self):
        llm = LangchainGaiminAI()
        prompt_template = "Qual é a capital da França?"
        prompt = ChatPromptTemplate.from_template(prompt_template)

        chain = prompt | llm

        response = chain.invoke({"question": "What is LangChain?"})

        self.assertIsNotNone(response)
        self.assertTrue(len(response) > 0)

    def test_llm_embed_success(self):
        embedding_model = LangchainGaiminEmbeddings()
        prompt_template = "Qual é a capital da França?"
        embeddings = asyncio.run(embedding_model.aembed_query(prompt_template))

        self.assertIsInstance(embeddings, list)
        self.assertGreater(len(embeddings), 0)

if __name__ == '__main__':
    unittest.main()

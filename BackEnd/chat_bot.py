from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
import os

class ChatBot:
    def _init_(self):
        self.api_key = None
        # self.llm = ChatOpenAI(model="gpt-4o-mini", api_key=self.api_key)
        self.llm=None
        # self.embeddings = OpenAIEmbeddings(api_key=self.api_key)
        self.embeddings=None
        self.vector_store = None

bot = ChatBot()
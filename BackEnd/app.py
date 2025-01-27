from fastapi import FastAPI, Request
from pydantic import BaseModel
from langchain_community.document_loaders import YoutubeLoader
from langchain_community.document_loaders.youtube import TranscriptFormat
from langgraph.checkpoint.memory import MemorySaver
from l_graph import graph_builder
from chat_bot import bot
from langchain_chroma import Chroma
import os
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings

app = FastAPI()
memory = MemorySaver()
graph = graph_builder.compile(checkpointer=memory)

# Specify an ID for the thread
mem_config = {"configurable": {"thread_id": "abc123"}}

class APIKeyRequest(BaseModel):
    api_key: str

class YouTubeURLRequest(BaseModel):
    url: str

class InputMessageRequest(BaseModel):
    message: str

@app.post("/set_openai_api_key/")
def set_openai_api_key(request: APIKeyRequest):
    global bot
    bot.api_key = request.api_key
    bot.llm = ChatOpenAI(model="gpt-4o-mini", api_key=request.api_key)
    bot.embeddings = OpenAIEmbeddings(api_key=request.api_key)    
    os.environ["OPENAI_API_KEY"] = request.api_key
    # Reinitialize the config to use the new API key
    return {"message": "OpenAI API key set successfully"}

@app.post("/load_youtube_transcript/")
def load_youtube_transcript(request: YouTubeURLRequest):
    global bot
    loader = YoutubeLoader.from_youtube_url(
        request.url,
        transcript_format=TranscriptFormat.CHUNKS,
        chunk_size_seconds=60,
    )
    all_splits = loader.load()
    bot.vector_store = Chroma.from_documents(documents=all_splits, embedding=bot.embeddings)
    
    return {"message": "YouTube transcript loaded successfully"}

@app.post("/process_input_message/")
def process_input_message_endpoint(request: InputMessageRequest):
    input_message = request.message
    response_message = ""
    for step in graph.stream(
        {"messages": [{"role": "user", "content": input_message}]},
        stream_mode="values",
        config=mem_config,
    ):
        step["messages"][-1].pretty_print()
        response_message = step["messages"][-1].content
    return {"message": response_message}

@app.get("/")
def greet_json():
    return {"Hello": "World!"}
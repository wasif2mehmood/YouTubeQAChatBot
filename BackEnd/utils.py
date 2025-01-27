from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain_core.tools import tool
from langchain_core.messages import SystemMessage
from langgraph.prebuilt import ToolNode
from langgraph.graph import MessagesState
from fastapi import HTTPException
from chat_bot import bot

def format_docs(docs):
    formatted_docs = []
    for doc in docs:
        metadata_str = ", ".join(f"{key}: {value}" for key, value in doc.metadata.items())
        formatted_docs.append(f"{doc.page_content}\nMetadata: {metadata_str}")
    return "\n\n".join(formatted_docs)

# Tool for retrieving context
@tool(response_format="content_and_artifact")
def retrieve(query: str):
    """Retrieve information related to a query."""
    if bot.vector_store is None:
        raise HTTPException(status_code=400, detail="YouTube transcript not loaded")
    retriever_from_llm = MultiQueryRetriever.from_llm(
        retriever=bot.vector_store.as_retriever(), llm=bot.llm)
    retrieved_docs = retriever_from_llm.invoke(query)
    serialized = format_docs(retrieved_docs)
    return serialized, retrieved_docs

# Generate an AIMessage that may include a tool-call to be sent or directly generate response without context retrieval if info required is in the chat memory.
def query_or_respond(state: MessagesState, llm, vector_store):
    llm_with_tools = llm.bind_tools([retrieve])
    response = llm_with_tools.invoke(state["messages"])
    print(response)
    return {"messages": [response]}

# Execute the retrieval if it's called.
tools = ToolNode([retrieve])

# Generate a response using the retrieved content.
def generate(state: MessagesState, llm):
    recent_tool_messages = []
    for message in reversed(state["messages"]):
        if message.type == "tool":
            recent_tool_messages.append(message)
        else:
            break
    tool_messages = recent_tool_messages[::-1]

    docs_content = "\n\n".join(doc.content for doc in tool_messages)
    system_message_content = (
        "You are an assistant for question-answering tasks. "
        "Use the following pieces of retrieved context to answer "
        "the question. If you don't know the answer, say that you "
        "don't know. Use three sentences maximum and keep the "
        "answer concise. Also return accurate timestamps from where"
        "you are extracting the answer in this format (start_seconds:----)"
        "\n\n"
        f"{docs_content}"
    )
    conversation_messages = [
        message
        for message in state["messages"]
        if message.type in ("human", "system")
        or (message.type == "ai" and not message.tool_calls)
    ]
    prompt = [SystemMessage(system_message_content)] + conversation_messages

    response = llm.invoke(prompt)
    return {"messages": [response]}
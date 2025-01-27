from langgraph.graph import END, START
from langgraph.prebuilt import tools_condition
from langgraph.graph import MessagesState, StateGraph
from chat_bot import bot
from utils import query_or_respond, tools, generate

graph_builder = StateGraph(MessagesState)
graph_builder.add_node("query_or_respond", lambda state: query_or_respond(state, bot.llm, bot.vector_store))
graph_builder.add_node("tools", lambda state: tools)
graph_builder.add_node("generate", lambda state: generate(state, bot.llm))

graph_builder.add_edge(START, "query_or_respond")
graph_builder.add_conditional_edges(
    "query_or_respond",
    tools_condition,
    {END: END, "tools": "tools"},
)
graph_builder.add_edge("tools", "generate")
graph_builder.add_edge("generate", END)
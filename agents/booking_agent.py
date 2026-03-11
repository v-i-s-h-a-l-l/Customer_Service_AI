from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent

from config import OPENAI_API_KEY, LLM_MODEL
from agents.tools import reserve_table


# ================================
# LLM
# ================================

llm = ChatOpenAI(model=LLM_MODEL, temperature=0, api_key=OPENAI_API_KEY)


# ================================
# TOOLS
# ================================

tools = [reserve_table]


# ================================
# LANGGRAPH REACT AGENT
# ================================

booking_agent = create_react_agent(llm, tools)


# ================================
# FUNCTION CALLED FROM rag_pipeline
# ================================


def run_booking_agent(query: str):
    result = booking_agent.invoke({"messages": [HumanMessage(content=query)]})

    return result["messages"][-1].content

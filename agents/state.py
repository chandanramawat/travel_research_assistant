from typing import TypedDict,Annotated
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
import operator
class AgentState(TypedDict):
    """this is type to short term memory which is used is circulate in every node and every read the data and update the data"""
    messages: Annotated[list[BaseMessage], add_messages]
    # it store the question information which come from user
    question:str
    # it store the response which come from research node
    research_result:str
    # it store the weather information 
    weather_result:str
    # it store the final answer
    final_answer:str
    # it store the tool information which tool is used
    tool_used: str

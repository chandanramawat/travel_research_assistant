from langchain_community.tools import tavily_search # tavily search is predefined tool in langchain framework 
from dotenv import load_dotenv
load_dotenv()
tavily_tool=tavily_search(max_result=3,
                                description=("Use this tool to seach in web and fetch real time data " \
                                "regarding hotel information,cap booking ,resturants and travel tip ")
)

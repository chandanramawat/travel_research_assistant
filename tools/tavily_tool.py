from langchain_community.tools import TavilySearchResults # tavily search is predefined tool in langchain framework 
from dotenv import load_dotenv
load_dotenv()
tavily_tool=TavilySearchResults(max_result=3,
                                description=("Use this tool to seach in web and fetch real time data " \
                                "regarding hotel information,cap booking ,resturants and travel tip ")
)

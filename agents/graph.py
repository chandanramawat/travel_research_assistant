from langchain_groq import ChatGroq
from dotenv import load_dotenv
load_dotenv()
LLM=ChatGroq(model="llama-3.1-8b-instant")
response=LLM.invoke("what is the top most travel city in rajasthan ")
print(response.content)
print("groq LLM working correctly")
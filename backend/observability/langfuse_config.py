import os
from dotenv import load_dotenv

load_dotenv()

print("PUBLIC KEY EXISTS:", bool(os.getenv("LANGFUSE_PUBLIC_KEY")))
print("SECRET KEY EXISTS:", bool(os.getenv("LANGFUSE_SECRET_KEY")))
print("HOST:", os.getenv("LANGFUSE_HOST"))

from langfuse import get_client
from langfuse.langchain import CallbackHandler

langfuse_client = get_client()
langfuse_handler = CallbackHandler()

def check_langfuse_config():
    if langfuse_client.auth_check():
        print("Langfuse connected successfully")
    else:
        print("Langfuse auth failed — check your keys/host")

if __name__ == "__main__":
    check_langfuse_config()
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

try:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    print("API key is valid!")
except Exception as e:
    print(f"Error: {e}")
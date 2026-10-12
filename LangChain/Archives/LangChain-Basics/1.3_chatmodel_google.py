from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

model = ChatGoogleGenerativeAI(
    model = 'gemini-1.5-pro'
)

result = model.invoke("What is the capital of France?")

print(result.content)


from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

embeddings = OpenAIEmbeddings(
    model = "text-embedding-3-large",
    dimensions=32
)

documents = [
    "Iron Man is a superhero in the Marvel Universe.",
    "Spider-Man is a superhero in the Marvel Universe.",
    "Batman is a superhero in the DC Universe."
]

result = embeddings.embed_documents(documents)

print(str(result))

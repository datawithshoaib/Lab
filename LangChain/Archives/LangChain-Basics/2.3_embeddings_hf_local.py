from langchain_huggingface import HuggingFaceEmbeddings

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

documents = [
    "Iron Man is a superhero in the Marvel Universe.",
    "Spider-Man is a superhero in the Marvel Universe.",
    "Batman is a superhero in the DC Universe."
]

result = embeddings.embed_documents(documents)

print(str(result))


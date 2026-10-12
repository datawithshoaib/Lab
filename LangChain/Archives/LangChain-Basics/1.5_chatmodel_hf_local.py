from langchain_huggingface import ChatHuggingFace, HuggingFacePipeline

llm = HuggingFacePipeline.from_model_id(
    model_id="Qwen/Qwen3-8B",
    task="text-generation",
    pipeline_kwargs={"temperature": 0.5, "max_new_tokens": 100},
)

model = ChatHuggingFace(
    llm = llm
)

result = model.invoke("What is the capital of France?")

print(result.content)


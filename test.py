import lmstudio as lms

model = lms.llm("mistralai/mistral-7b-instruct-v0.3")
result = model.respond("What is the meaning of life?")

print(result)

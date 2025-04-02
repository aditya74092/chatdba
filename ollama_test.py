from langchain_community.llms import Ollama

llm = Ollama(model="llama3:8b")
response = llm.invoke("How to count users in SQL?")
print(response)
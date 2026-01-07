from llama_index.llms.ollama import Ollama


def generate_insights():
    model_name = 'llama3.1:8b'
    question = str(input('write your question here: '))
    llm = Ollama(model=model_name, request_timeout=120)
    response = llm.complete(question)

    return response

print(generate_insights())
print('done')
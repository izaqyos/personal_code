import ollama

stream = ollama.chat(
        model = 'mistral',
        messages = [{'role':'user','content':'why is the sky blue'}],
                    stream=True)

for chunk in stream:
    print(chunk['message']['content'], end='', flush=True)

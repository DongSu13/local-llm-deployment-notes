from ollama import generate

response = generate('deepseek-local-demo', 'Why is the sky blue?')
print(response['response'])

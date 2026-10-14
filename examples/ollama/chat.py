from ollama import chat

messages = [
  {
    'role': 'user',
    'content': 'Why is the sky blue?',
  },
]

response = chat('deepseek-local-demo', messages=messages)
print(response['message']['content'])

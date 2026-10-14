from ollama import generate

for part in generate('deepseek-local-demo', 'Why is the sky blue?', stream=True):
  print(part['response'], end='', flush=True)

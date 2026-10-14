from ollama import Client

client = Client()
response = client.create(
  model='my-assistant',
  from_='deepseek-local-demo',
  system='You are a helpful local assistant.',
  stream=False,
)
print(response.status)

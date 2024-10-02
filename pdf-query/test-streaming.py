from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

from dotenv import load_dotenv


load_dotenv()

chat = ChatOpenAI(streaming=True)

prompt = ChatPromptTemplate.from_messages([
    ('human', '{content}')
])

messages = prompt.format_messages(content="tell me a joke")
# print(messages)

# no streaming
# output = chat(messages)
# print(output)

# streaming from langchain to the app
output = chat.stream(messages)  # stream() forces streaming capability no matter what streaming flag in ChatOpenAI instant is True/False 
# print(output)

for o in output:
  print(o.content)
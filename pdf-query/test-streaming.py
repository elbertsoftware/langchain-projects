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

output = chat(messages)
print(output)
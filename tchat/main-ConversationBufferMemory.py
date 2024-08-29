from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder, HumanMessagePromptTemplate
from langchain.memory import ConversationBufferMemory, FileChatMessageHistory  # there are many other storage for chat history in langchain, not just file as implemented here

from dotenv import load_dotenv

load_dotenv()

chat = ChatOpenAI()

memory = ConversationBufferMemory(
  chat_memory=FileChatMessageHistory('messages.json'),  # file stored history of chats
  memory_key='messages',  # the dict key name for storing previous chats
  return_messages=True  # return the 'messages' as an array of intelligent langchain defined objects
)

prompt = ChatPromptTemplate(
  input_variables=[
    'content',
    'messages'
  ],
  messages=[
    MessagesPlaceholder(variable_name='messages'),
    HumanMessagePromptTemplate.from_template('{content}')
  ]
)

chain = LLMChain(
  llm=chat,
  prompt=prompt,
  memory=memory
)

while True:
  content = input('>> ')

  result = chain({
    "content": content
  })

  print(result['text'])
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder, HumanMessagePromptTemplate
from langchain.memory import ConversationSummaryMemory  #, FileChatMessageHistory  # there are many other storage for chat history in langchain, not just file as implemented here

from dotenv import load_dotenv

load_dotenv()

chat = ChatOpenAI(
  verbose=True  # enable 'debug' mode
)

memory = ConversationSummaryMemory(
  # chat_memory=FileChatMessageHistory('messages.json'),  # file stored history of chats, does not work well with ConversationSummaryMemory for now
  memory_key='messages',  # the dict key name for storing previous chats
  return_messages=True,  # return the 'messages' as an array of intelligent langchain defined objects
  llm=chat  # the language model to be used for summary
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
  memory=memory,
  verbose=True  # enable 'debug' mode
)

while True:
  content = input('>> ')

  result = chain({
    "content": content
  })

  print(result['text'])
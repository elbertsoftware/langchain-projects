from typing import Any
from uuid import UUID
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from langchain.callbacks.base import BaseCallbackHandler

from dotenv import load_dotenv
from langchain_core.outputs import ChatGenerationChunk, GenerationChunk


class StreamingHandler(BaseCallbackHandler):
  def on_llm_new_token(self, token, **kwargs):
    print(token)


load_dotenv()

chat = ChatOpenAI(
  streaming=True,
  callbacks=[StreamingHandler()]
)

prompt = ChatPromptTemplate.from_messages([
    ('human', '{content}')
])

chain = LLMChain(
  llm=chat,
  prompt=prompt
)

# messages = prompt.format_messages(content="tell me a joke")
# print(messages)

# 1. no streaming with direct language mode
# output = chat(messages)
# print(output)

# 2. streaming with direct language model from langchain to the app
# output = chat.stream(messages)  # stream() forces streaming capability no matter what streaming flag in ChatOpenAI instant is True/False 
# print(output)

# for o in output:
#   print(o.content)

# 3. no stream with chain
# output = chain('tell me a joke')
# print(output)

# 4. non implemented default streaming with chain
output = chain.stream(
  input={
    'content': 'tell me a joke'
  }
)

# print(output)
for o in output:
  print(o)
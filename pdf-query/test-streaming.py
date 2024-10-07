from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain, ConversationalRetrievalChain
from langchain.callbacks.base import BaseCallbackHandler

from dotenv import load_dotenv
from queue import Queue
from threading import Thread


class StreamingHandler(BaseCallbackHandler):
  def __init__(self, queue):
    self.queue = queue

  def on_llm_new_token(self, token, **kwargs):
    # streaming tokens arrive one by one
    # print(token)
    self.queue.put(token)

  def on_llm_end(self, response, **kwargs):
    self.queue.put(None)  # ending the while loop below since there is no more streaming

  def on_llm_error(self, error, **kwargs):
    self.queue.put(None)  # ending the while loop below in case of error


load_dotenv()

chat = ChatOpenAI(
  streaming=True
  # callbacks=[StreamingHandler()]
)

prompt = ChatPromptTemplate.from_messages([
    ('human', '{content}')
])

# chain = LLMChain(
#   llm=chat,
#   prompt=prompt
# )

# messages = prompt.format_messages(content="tell me a joke")
# print(messages)

# 1. no streaming from a LLM
# output = chat(messages)
# print(output)

# 2. streaming directly from a LLM (langchain to the app)
# output = chat.stream(messages)  # stream() forces streaming capability no matter what streaming flag in ChatOpenAI instant is True/False 
# print(output)

# for o in output:
#   print(o.content)

# 3. no stream from a chain
# output = chain('tell me a joke')
# print(output)

# 4. non implemented default streaming from a chain
# output = chain.stream(
#   input={
#     'content': 'tell me a joke'
#   }
# )

# # print(output)
# for o in output:
#   print(o)

# 5. Streaming from a chain

# Mixin approach!
class StreamableChain:
  def stream(self, input):
    queue = Queue()
    handler = StreamingHandler(queue)

    # make sure the stream method should run the chain 
    # but it's not gonna work since it waits for full response before executing the next line of code
    # which is handling actual streaming
    # self(input) 

    # using thread to solve the issue mentioned above
    def task():
      self(
        input,
        callbacks=[handler]
      )

    Thread(target=task).start()  # run this on a seperate thread

    # print('hi there')

    # test returning a generator that produces strings
    # yield 'hi'
    # yield ' there'

    # yield tokens from StreamingHandler's on_llm_new_token() callback into the generator
    while True:
      token = queue.get()
      if token is None:
        break
      
      yield token


class StreamingChain(StreamableChain, LLMChain):
  pass


class StreamingConversationalRetrievalChain(StreamableChain, ConversationalRetrievalChain):
  pass


chain = StreamingChain(
  llm=chat,
  prompt=prompt
)

# print(chain('tell me a joke'))  # no streaming part is still working
for output in chain.stream(input={'content': 'tell me a joke'}):
  print(output)
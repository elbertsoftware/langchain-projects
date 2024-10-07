from langchain.callbacks.base import BaseCallbackHandler


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
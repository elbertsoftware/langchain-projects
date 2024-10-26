from langchain.callbacks.base import BaseCallbackHandler


class StreamingHandler(BaseCallbackHandler):
  def __init__(self, queue):
    self.queue = queue
    self.streaming_run_ids = set()

  def on_chat_model_start(self, serialized, messages, run_id, **kwargs):
    # print(serialized)
    # print(run_id)
    if serialized['kwargs']['streaming']:
      # print('Streaming model: should listen to events with a run_id of', run_id)
      self.streaming_run_ids.add(run_id)

  def on_llm_new_token(self, token, **kwargs):
    # streaming tokens arrive one by one
    # print(token)
    self.queue.put(token)

  def on_llm_end(self, response, run_id, **kwargs):
    if run_id in self.streaming_run_ids:
      self.queue.put(None)  # ending the while loop below since there is no more streaming
      self.streaming_run_ids.remove(run_id)

  def on_llm_error(self, error, run_id, **kwargs):
    if run_id in self.streaming_run_ids:
      self.queue.put(None)  # ending the while loop below in case of error
      self.streaming_run_ids.remove(run_id)
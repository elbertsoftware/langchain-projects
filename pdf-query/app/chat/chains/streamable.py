
from queue import Queue
from threading import Thread

from flask import current_app

from app.chat.callbacks.stream import StreamingHandler


class StreamableChain:
  def stream(self, input):
    queue = Queue()
    handler = StreamingHandler(queue)

    def task(app_context):
      app_context.push()  # add the thread into the existing flask webapp's content

      self(
        input,
        callbacks=[handler]
      )

    Thread(
      target=task, 
      args=[current_app.app_context()]  # make sure the thread will be part of the flask webapp's context
    ).start()  # run this on a seperate thread

    while True:
      token = queue.get()
      if token is None:
        break
      
      yield token
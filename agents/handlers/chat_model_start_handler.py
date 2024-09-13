from langchain.callbacks.base import BaseCallbackHandler

from pyboxen import boxen

# print(
#   boxen("text here", title='Title', color='yellow')
# )

def boxen_print(*args, **kwargs):
  print(boxen(*args, **kwargs))

# boxen_print('text here', title='Title', color='red')

class ChatModelStartHandler(BaseCallbackHandler):
  def on_chat_model_start(self, serialized, messages, **kwargs):
    # print(messages)
    print('\n\n========= Sending Messages =========\n\n')

    for message in messages[0]:  # there is not message batching yet, so there is only one array of messages
      if message.type == 'system':
        boxen_print(message.content, title=message.type, color='yellow')

      elif message.type == 'human':
        boxen_print(message.content, title=message.type, color='green')

      elif message.type == 'ai' and 'function_call' in message.additional_kwargs:
        function_call = message.additional_kwargs['function_call']
        boxen_print(
          f'Running tool {function_call["name"]} with args {function_call["arguments"]}', 
          title=message.type, 
          color='cyan'
        )

      elif message.type == 'ai':
        boxen_print(message.content, title=message.type, color='blue')

      elif message.type == 'function':
        boxen_print(message.content, title=message.type, color='purple')

      else:
        boxen_print(message.content, title=message.type, color='orange')
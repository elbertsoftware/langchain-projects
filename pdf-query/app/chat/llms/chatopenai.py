from langchain.chat_models import ChatOpenAI


def build_llm(char_args, model_name):
  return ChatOpenAI(
    streaming=char_args.streaming,
    model_name=model_name  # 'gpt-3.5-turbo' is used default
  )
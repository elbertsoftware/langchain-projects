from langchain.chat_models import ChatOpenAI

from app.chat.models import ChatArgs
from app.chat.vector_stores import retriever_map
from app.chat.llms.chatopenai import build_llm
from app.chat.memories.sql_memory import build_memory
from app.chat.chains.retrieval import StreamingConversationalRetrievalChain
from app.web.api import set_conversation_components, get_conversation_components

import random


def build_chat(chat_args: ChatArgs):
    """
    :param chat_args: ChatArgs object containing
        conversation_id, pdf_id, metadata, and streaming flag.

    :return: A chain

    Example Usage:

        chain = build_chat(chat_args)
    """

    components = get_conversation_components(chat_args.conversation_id)
    previous_retriever = components['retriever']

    retriever = None
    if previous_retriever:
        # this is NOT the first message of the conversation
        # gonna use the same retriever
        build_retriever = retriever_map[previous_retriever]
        retriever = build_retriever(chat_args)
    else:
        # this is the first message of the conversation
        # gonna pick a random retriever to use
        random_retriever_name = random.choice(list(retriever_map.keys()))

        build_retriever = retriever_map[random_retriever_name]
        retriever = build_retriever(chat_args)

        set_conversation_components(
            conversation_id=chat_args.conversation_id,
            llm='',
            memory='',
            retriever=random_retriever_name
        )

    return StreamingConversationalRetrievalChain.from_llm(
        llm=build_llm(chat_args),
        memory=build_memory(chat_args),
        retriever=retriever, 

        # specify a separate LLM for the internal condense question chain to use
        # instead of sharing the same chain with combine doc chain
        condense_question_llm=ChatOpenAI(streaming=False) 
    )

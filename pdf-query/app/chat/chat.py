from langchain.chat_models import ChatOpenAI

from app.chat.models import ChatArgs
from app.chat.llms import llm_map
from app.chat.memories import memory_map
from app.chat.vector_stores import retriever_map
from app.chat.chains.retrieval import StreamingConversationalRetrievalChain
from app.web.api import set_conversation_components, get_conversation_components

import random


def select_component(component_type, component_map, chat_args):
    components = get_conversation_components(chat_args.conversation_id)
    previous_component = components[component_type]

    if previous_component:
        # this is NOT the first message of the conversation
        # gonna use the same component
        builder = component_map[previous_component]
        return previous_component, builder(chat_args)
    else:
        # this is the first message of the conversation
        # gonna pick a random component to use
        random_component_name = random.choice(list(component_map.keys()))

        builder = component_map[random_component_name]
        return random_component_name, builder(chat_args)

def build_chat(chat_args: ChatArgs):
    """
    :param chat_args: ChatArgs object containing
        conversation_id, pdf_id, metadata, and streaming flag.

    :return: A chain

    Example Usage:

        chain = build_chat(chat_args)
    """

    llm_name, llm = select_component('llm', llm_map, chat_args)
    memory_name, memory = select_component('memory', memory_map, chat_args)
    retriever_name, retriever = select_component('retriever', retriever_map, chat_args)

    print(f'Running chain with llm:\n\t{llm_name}\n\tmemory: {memory_name}\n\tretriever: {retriever_name}')
    set_conversation_components(
        conversation_id=chat_args.conversation_id,
        llm=llm_name,
        memory=memory_name,
        retriever=retriever_name
    )

    return StreamingConversationalRetrievalChain.from_llm(
        llm=llm,
        memory=memory,
        retriever=retriever, 

        # specify a separate LLM for the internal condense question chain to use
        # instead of sharing the same chain with combine doc chain
        condense_question_llm=ChatOpenAI(streaming=False) 
    )

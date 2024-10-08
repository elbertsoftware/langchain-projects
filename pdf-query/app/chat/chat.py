from langchain.chat_models import ChatOpenAI

from app.chat.models import ChatArgs
from app.chat.vector_stores.pinecone import build_retriever
from app.chat.llms.chatopenai import build_llm
from app.chat.memories.sql_memory import build_memory
from app.chat.chains.retrieval import StreamingConversationalRetrievalChain


def build_chat(chat_args: ChatArgs):
    """
    :param chat_args: ChatArgs object containing
        conversation_id, pdf_id, metadata, and streaming flag.

    :return: A chain

    Example Usage:

        chain = build_chat(chat_args)
    """
    
    return StreamingConversationalRetrievalChain.from_llm(
        llm=build_llm(chat_args),
        memory=build_memory(chat_args),
        retriever=build_retriever(chat_args),

        # specify a separate LLM for the internal condense question chain to use
        # instead of sharing the same chain with combine doc chain
        condense_question_llm=ChatOpenAI(streaming=False) 
    )

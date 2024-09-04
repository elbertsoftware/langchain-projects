from dotenv import load_dotenv

from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores.chroma import Chroma
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI

load_dotenv()

embeddings = OpenAIEmbeddings()

db = Chroma(
  persist_directory='emb',  # where is the db folder
  embedding_function=embeddings  # function to be used for embedding
)

retriever = db.as_retriever()

chat = ChatOpenAI()

chain = RetrievalQA.from_chain_type(
  llm=chat,
  retriever=retriever,
  chain_type='stuff'
)

result = chain.run('What is an interesting fact about the English language?')
print(result)
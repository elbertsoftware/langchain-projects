from dotenv import load_dotenv

from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores.chroma import Chroma
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI

from redundant_filter_retriever import RedundantFilterRetriever

# enable debug mode
# import langchain
# langchain.debug = True

load_dotenv()

embeddings = OpenAIEmbeddings()

db = Chroma(
  persist_directory='emb',  # where is the db folder
  embedding_function=embeddings  # function to be used for embedding
)

# retriever = db.as_retriever()
# use custom retriever instead
retriever = RedundantFilterRetriever(
  embeddings=embeddings,
  chroma=db
)

chat = ChatOpenAI()

chain = RetrievalQA.from_chain_type(  # Ctrl + click to view source code
  llm=chat,
  retriever=retriever,
  chain_type='stuff',  # take some context from the vector store and 'stuff' it into the prompt
  #chain_type='map_reduce',
  #chain_type='map_rerank',
  #chain_type='refine',
  #verbose=True  # bug in langchain, does not work, enable global debug as above
)

result = chain.run('What is an interesting fact about the English language?')
print(result)
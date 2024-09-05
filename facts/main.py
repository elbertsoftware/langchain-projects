from dotenv import load_dotenv

from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores.chroma import Chroma

load_dotenv()

text_splitter = CharacterTextSplitter(
  separator='\n',
  chunk_size=200,  # chunk size takes place first then seperator
  chunk_overlap=0
)

loader = TextLoader('facts.txt')
docs = loader.load_and_split(
  text_splitter=text_splitter
)

# print(docs)
for doc in docs:
  print(doc.page_content, '\n')

embeddings = OpenAIEmbeddings()

# embedding = embeddings.embed_query('hi there')
# print(embedding)

# ChromaDb will reach out to OpenAI and calculate embedded vectors for each chunk of text (docs) using the the assigned embeddings
# this approach costs a very small amount of money since embedded vectors eventually stored into SQLite
db = Chroma.from_documents(
  docs, 
  embedding=embeddings,
  persist_directory='emb'  # the folder where data is stored
)

results = db.similarity_search_with_score(
  'What is an interesting fact about the English language?',
  k=4  # number of results returned
)

for result in results:
  print('\n')
  print(result[1])  # the score
  print(result[0].page_content)  # k = 1 returns the most relevant one
from dotenv import load_dotenv

from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings

load_dotenv()

embeddings = OpenAIEmbeddings()

# embedding = embeddings.embed_query('hi there')
# print(embedding)

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
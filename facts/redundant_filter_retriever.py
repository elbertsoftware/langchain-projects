from langchain.schema import BaseRetriever
from langchain.embeddings.base import Embeddings
from langchain.vectorstores.chroma import Chroma

class RedundantFilterRetriever(BaseRetriever):
  embeddings: Embeddings
  chroma: Chroma

  def get_relevant_documents(self, query):
    # calculate embedding of the query
    emb = self.embeddings.embed_query(query)

    # look for relevant docs with a threashold of filtering similar docs
    return self.chroma.max_marginal_relevance_search_by_vector(
      embedding=emb,
      lambda_mult=0.5  # higher values allow similar documents
    )
  
  async def aget_relevant_documents(self):
    return []

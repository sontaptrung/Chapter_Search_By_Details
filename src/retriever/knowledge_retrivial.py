from vector_database import QdrantEngine
from typing import List
class KnowledgeRetriever:
    def __init__(self,vector_db:QdrantEngine) -> None:
        self.vector_db = vector_db
    def run(self, query:str) -> List[str]:
        documents = self.vector_db.search(query)
        contexts = [doc.page_content for doc in documents]
        return contexts
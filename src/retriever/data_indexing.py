from indexing import Chunker, JsonParser
from vector_database import QdrantEngine
from typing import List
from langchain_core.documents import Document
from embedding import MultilingualE5Large


class DataParsing:
    @staticmethod
    def run(data_path: str, embedding_client: MultilingualE5Large):
        list_doc = JsonParser.run(data_path=data_path)
        chunks, ids = Chunker.run(documents=list_doc, embedding_client=embedding_client)
        return chunks, ids


class DataInsertion:
    def __init__(self, vector_db: QdrantEngine) -> None:
        self.vector_db = vector_db

    def run(self, chunks: List[Document], ids: List[int]):
        self.vector_db.add_documents(chunks, ids=ids)

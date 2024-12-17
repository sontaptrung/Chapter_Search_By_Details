from .base import BaseVectorDBEngine
from loguru import logger
from typing import Any, Dict, List
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams

class QdrantEngine(BaseVectorDBEngine):
    """
    Qdrant Engine for managing vector storage and document retrieval.
    Provides an interface to the Qdrant database, facilitating operations such as search, insert, and delete.
    """

    def __init__(
        self,
        embedding_function: Embeddings,
        collection_name: str,
        host: str = "http://localhost",
        port: int = 6333,
        top_k: int = 10,
        search_type: str = "mmr"
    ):
        """
        Initialize the QdrantEngine class.

        Args:
            embedding_function (Embeddings): The embedding model used for vectorizing documents.
            collection_name (str): The name of the collection in the Qdrant database.
            host (str): The hostname where the Qdrant server is running.
            port (int): The port number on which the Qdrant server is accessible.
        """
        self._collection_name = collection_name
        self._url = f"{host}:{port}"
        self._embedding = embedding_function
        self._client = QdrantClient(url=self._url)
        self._top_k = top_k
        self._search_type = search_type

        # Check if the collection exists, and create it if it doesn't
        try:
            self._client.get_collection(collection_name=self._collection_name)
        except Exception as err:
            logger.info(f"Getting the collecting meets errors {str(err)}")
            self._client.create_collection(
                collection_name=self._collection_name,
                vectors_config=VectorParams(size=1024, distance=Distance.COSINE),
            )
        # initialize qdrant client
        self._qdrant = QdrantVectorStore.from_existing_collection(
            embedding=self._embedding,
            collection_name=self._collection_name,
            url=self._url,
        )

    def search(self, query: str, **kwargs: Dict[str, Any]) -> List[Document]:
        """
        Search for documents in the Qdrant vector database using a text query.

        Args:
            query (str): A string query for searching documents.
            **kwargs (dict): Additional keyword arguments for search parameters.

        Returns:
            List[Document]: A list of documents matching the query.
        """
        try:
            results = self._qdrant.search(
                                query=query,
                                search_type=self._search_type,
                                k=self._top_k,
                                **kwargs)
            return results
        except Exception as e:
            logger.error(f"Error during search: {str(e)}")
            return []

    def add_documents(self, documents: List[Document], ids: List[int]):
        """
        Add documents to the Qdrant database.

        Args:
            documents (List[Document]): A list of Document objects to be added to the database.
        """
        try:
            self._qdrant.add_documents(documents=documents, ids=ids, batch_size=32)
            logger.info(f"Added {len(documents)} documents to Qdrant")
        except Exception as err:
            logger.error(f"Qdrant: Database Insertion Fail\nDetail: {str(err)}")

    def remove_documents(self, ids: List[str]):
        """
        Remove documents from the Qdrant database by their IDs.

        Args:
            ids (List[str]): A list of document IDs to be removed.
        """
        try:
            self._qdrant.delete(ids=ids)
            logger.info(f"Removed {len(ids)} documents from Qdrant")
        except Exception as err:
            logger.error(f"Qdrant: Database Removal Fail\nDetail: {str(err)}")
            
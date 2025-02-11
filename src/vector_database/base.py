from abc import ABC, abstractmethod
from typing import Dict, List, Any
from langchain_core.documents import Document


class BaseVectorDBEngine(ABC):
    """Abstract base class for a vector database"""

    @abstractmethod
    def add_documents(self, documents: List[Document], ids: List[int]):
        """
        Add documents to the database
        """
        raise NotImplementedError

    @abstractmethod
    def remove_documents(self, ids: List[str]):
        """
        Remove documents to the documents
        """
        raise NotImplementedError
    
    @abstractmethod
    def search(self, query: str, **kwargs: Dict[str, Any]) -> List[Document]:
        """
        Search the database based on the given query.

        Args:
            query (str): The search query.
            **kwargs (Dict[str, Any]): Additional keyword arguments for the search.

        Returns:
            List[Any]: A list of search results.
        """
        raise NotImplementedError
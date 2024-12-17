from typing import List
from langchain_core.documents import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from embedding import MultilingualE5Large

class Chunker:
    @staticmethod
    def run(documents: List[Document], embedding_client: MultilingualE5Large):
        final_chunks = []
        ids = []
        # Load each chapter
        for chapter_id, doc in enumerate(documents, start=1):
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=750,
                chunk_overlap=50,
                # length_function=embedding_client.calculate_token,
            )
            chunks = text_splitter.split_text(
                doc.page_content.lstrip(doc.metadata.get("title")).strip()
            )
            for chunk_id, chunk in enumerate(chunks, start=1):
                text_splitter_for_chunk = RecursiveCharacterTextSplitter(
                    chunk_size=175,
                    chunk_overlap=0,
                    # length_function=embedding_client.calculate_token,
                )
                splitted_chunks = text_splitter_for_chunk.split_text(chunk)
                for split_chunk_id, splitted_chunk in enumerate(splitted_chunks, start=1):
                    # Tạo ID cho mỗi để đưa vào collection
                    point_id = int(f"{chapter_id}{chunk_id}{split_chunk_id}")
                    ids.append(point_id)
                    final_chunks.append(
                        Document(
                            page_content=splitted_chunk,
                            metadata={
                                "chunk_content":chunk,
                                "chapter_title": doc.metadata.get("chapter_title"),
                                "chapter_link": doc.metadata.get("chapter_link"),
                                "comic_title": doc.metadata.get("comic_title"),
                                "comic_link": doc.metadata.get("comic_link"),
                            },
                        )
                    )
        return final_chunks, ids

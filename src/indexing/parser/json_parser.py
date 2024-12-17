import json
from langchain_core.documents import Document
from typing import List


class JsonParser:
    @staticmethod
    def run(data_path) -> List[Document]:
        with open(data_path, "r", encoding="utf-8") as file:
            data = json.load(file)  # Load JSON data

        # Extract the list of chapters
        chapters = data.get("ListChuong", [])
        comic_title = data.get("TenComic", "Untitled")
        comic_link = data.get("LinkComic", "")
        documents = []

        # Prepare documents by extracting chapter title and content
        for chapter in chapters:
            chapter_title = chapter.get("TenChuong", "Untitled")
            chapter_content = chapter.get("NoiDung", "")
            chapter_link = chapter.get("LinkChuong", "")
            documents.append(
                Document(
                    page_content=chapter_content,
                    metadata={
                        "chapter_title": chapter_title,
                        "chapter_link": chapter_link,
                        "comic_title": comic_title,
                        "comic_link": comic_link,
                    },
                )
            )

        return documents

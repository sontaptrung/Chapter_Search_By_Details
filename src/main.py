from vector_database import QdrantEngine
from embedding import MultilingualE5Large
from retriever import DataParsing, DataInsertion, KnowledgeRetriever

def main():
    embedding_client = MultilingualE5Large(model="http://localhost:8080")
    vector_db_client = QdrantEngine(
        embedding_function=embedding_client, collection_name="pntt_10_chapter"
    )


    chunks, ids = DataParsing.run(
        data_path="/home/sontt/workspaces/craw_truyen/pntt_10_chapter.json",embedding_client=embedding_client
    )
    data_insersion = DataInsertion(vector_db=vector_db_client)
    data_insersion.run(chunks=chunks, ids=ids)

# input_query = """
# """

# retriever = KnowledgeRetriever(vector_db=vector_db_client).run(query=input_query)

if __name__ == '__main__':
    main()
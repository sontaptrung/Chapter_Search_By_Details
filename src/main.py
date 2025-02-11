from web import data_router, generate_router
from fastapi import FastAPI

app = FastAPI()


# Đăng ký router
app.include_router(data_router, prefix="/data_api")
# Đăng ký router từ generate_api
app.include_router(generate_router, prefix="/generate_api")
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

# def main():
#     embedding_client = MultilingualE5Large(model="http://localhost:8080")
#     vector_db_client = QdrantEngine(
#         embedding_function=embedding_client, collection_name="pntt_10_chapter"
#     )

#     # # indexing data
#     # chunks, ids = DataParsing.run(
#     #     data_path="/home/sontt/workspaces/craw_truyen/pntt_10_chapter.json",embedding_client=embedding_client
#     # )
#     # data_insersion = DataInsertion(vector_db=vector_db_client)
#     # data_insersion.run(chunks=chunks, ids=ids)
#     llm = Llama3Engine(base_url="http://localhost:8888/v1", # "http://<Your api-server IP>:port"
#     api_key = "sk-no-key-required",
#     temperature=0,
#     # model="gpt-3.5-turbo"
# )
#     query = "được tam thúc giới thiệu vào Thất Huyền môn"
#     generator_client = Generator(llm = llm).run(query=query, vector_db= vector_db_client)
#     print(generator_client)

# if __name__ == '__main__':
#     main()


from fastapi import APIRouter, HTTPException
from vector_database import QdrantEngine
from embedding import MultilingualE5Large
from llm import Llama3Engine
from generator import Generator
from pydantic import BaseModel
generate_router = APIRouter()

# curl -X 'POST' 'http://127.0.0.1:6666/generate_api/generate-answer' -H 'Content-Type: application/json' -d '{"question": "được tam thúc giới thiệu vào Thất Huyền môn"}'

embedding_client = MultilingualE5Large(model="http://localhost:8080")
vector_db_client = QdrantEngine(
    embedding_function=embedding_client, collection_name="pntt_10_chapter"
)
llm = Llama3Engine(base_url="http://localhost:8888/v1", # "http://<Your api-server IP>:port"
    api_key = "sk-no-key-required",
    temperature=0,
    # model="gpt-3.5-turbo"
)
generator = Generator(llm = llm,vector_db= vector_db_client)
# Định nghĩa schema cho dữ liệu đầu vào và đầu ra
class RequestData(BaseModel):
    question: str
    # collection: str
class ResponseData(BaseModel):
    answer: str

@generate_router.post("/generate-answer", response_model=ResponseData)
async def generate_answer(data: RequestData):
    """
    Nhận dữ liệu từ người dùng và trả về câu trả lời từ bot.
    """
    try:
        question = data.question
        answer = generator.run(query=question)
        return ResponseData(answer=answer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

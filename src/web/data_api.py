from vector_database import QdrantEngine
from embedding import MultilingualE5Large
from retriever import DataParsing, DataInsertion
from fastapi import APIRouter, UploadFile, HTTPException, File
import json

data_router = APIRouter()

# curl -X POST "http://127.0.0.1:6666/data_api/index-data" -H 'Content-Type: multipart/form-data' -F "file=@/home/sontt/workspaces/craw_truyen/pntt_10_chapter.json"

embedding_client = MultilingualE5Large(model="http://localhost:8080")
vector_db_client = QdrantEngine(
    embedding_function=embedding_client, collection_name="pntt_10_chapter"
)
data_insersion = DataInsertion(vector_db=vector_db_client)

@data_router.post("/index-data")
async def index_data(file: UploadFile = File(...)):
    """
    API để đọc dữ liệu từ file JSON, chunk và đưa vào database.
    """
    # Kiểm tra định dạng file
    if not file.filename.endswith(".json"):
        raise HTTPException(status_code=400, detail="Only JSON files are supported.")
    
    try:
        # Đọc nội dung file JSON
        contents = await file.read()
        data = json.loads(contents.decode('utf-8'))
        # Kiểm tra dữ liệu
        if not isinstance(data, dict):
            raise HTTPException(
                status_code=400, detail="Invalid JSON format."
            )
        # Chunk dữ liệu và lưu vào database
        # indexing data
        chunks, ids = DataParsing.run(data=data, embedding_client=embedding_client)
        data_insersion.run(chunks=chunks, ids=ids)
        return {"message": "Data indexed successfully."}

    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON file.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

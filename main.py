from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from groq import Groq
import chromadb
from dotenv import load_dotenv
load_dotenv()


app = FastAPI()
client = Groq()
chroma_client = chromadb.Client()
collection = chroma_client.create_collection("repair_collection")

class RepairHistory(BaseModel):
    repair_id: str = Field(min_length=1)
    text: str = Field(min_length=1)

class RepairHistoryQuery(BaseModel):
    query: str = Field(min_length=1)
    no_results: int

class EchoItem(BaseModel):
    text: str = Field(min_length=1)

class SummarizeRequest(BaseModel):
    text: str = Field(min_length=1)

class TranslateMessage(BaseModel):
    text: str = Field(min_length=1)
    language: str = Field(min_length=2)
    
@app.get("/")
async def root():
    return "hello"


@app.post("/echo")
async def echo_back(item: EchoItem):
    return {"text": item.text}


@app.post("/summarize")
async def summarize_text(item: SummarizeRequest):
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": f"summarize THIS: {item.text}",
                }
            ],
            model="llama-3.3-70b-versatile",
        )

        return {"summary":chat_completion.choices[0].message.content}

    except Exception as e:  
        raise HTTPException(status_code=500, detail=f"LLM CALL FAILED: {str(e)}")


@app.post("/translate")
async def translate_text(item: TranslateMessage):
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": f"Translate The Following text to {item.language}: {item.text}",
                }
            ],
            model="llama-3.3-70b-versatile",
        )

        return {"translation":chat_completion.choices[0].message.content}

    except Exception as e:  
        raise HTTPException(status_code=500, detail=f"LLM CALL FAILED: {str(e)}")



@app.post("/repair-history/add")
async def add_repair_history(item: RepairHistory):
    collection.add(
        documents=[item.text],
        ids=[item.repair_id]
    )



@app.post("/repair-history/search")
async def search_repair_history(item: RepairHistoryQuery):
    results = collection.query(query_texts=[item.query], n_results=item.no_results)
    return {"result": results['documents'][0]}





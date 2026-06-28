from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from groq import Groq
from dotenv import load_dotenv
load_dotenv()


app = FastAPI()
client = Groq()



class EchoItem(BaseModel):
    text: str

class SummarizeRequest(BaseModel):
    text: str

class TranslateMessage(BaseModel):
    text: str
    language: str
    
@app.get("/")
async def root():
    return "hello"


@app.post("/echo")
async def echo_back(item: EchoItem):
    return item.text


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



    



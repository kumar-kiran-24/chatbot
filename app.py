from fastapi import FastAPI,UploadFile,File, HTTPException
import uvicorn
from pydantic import BaseModel
from  fastapi.middleware.cors import CORSMiddleware
import os
import shutil


from main import Main
from src.components.ragchatbot import RagChatbot
from src.components.chatbot import Chatbot

app=FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*" ] , 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return{
        "status":"running"
    }

class chat_bot(BaseModel):
    question:str
    session_id:str

qa_bot=Chatbot()
main=Main()

@app.post("/chatbot")
async def chatbot(user:chat_bot):
    question=user.question
    session_id=user.session_id

    res=qa_bot.chat(question=question,session_id=session_id)
    print(res)
    return {
        "response":res
    }


class get_url(BaseModel):
    url:str


class rag_url(BaseModel):
    question:str
    session_id:str

rag=RagChatbot()
@app.post("/ragchatbot_url")
async def ragbot(user:rag_url):
    question=user.question
    session_id=user.session_id
    context=main.data_loader(question=question)
    print("context in the app",context)
    res=rag.ragchatbot(question=question,session_id=session_id,context=context)
    print(res)
    return{
        "response":res
    }
class web_data(BaseModel):
    url:str

@app.post("/web")
def web(url: web_data):
    print(url)
    if not url.url.startswith("http"):
        raise HTTPException(status_code=400, detail="Invalid URL format")

    main.web(url=url.url)

    return {
        "response": "upload successfully"
    }

UPLOAD_DIR = "tmp"



@app.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    try:
       
        if file.content_type != "application/pdf":
            raise HTTPException(status_code=400, detail="Only PDF files allowed")

        filename = f"{uuid.uuid4()}.pdf"
        file_path = os.path.join(UPLOAD_DIR, filename)
        print("file path",file_path)

     
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        emb=main.pdf(path=file_path)

        return {
            "response":"upload susefylly"
        }

    except Exception as e:
        return{
            "error":e
        }
class text_model(BaseModel):
    text:str
@app.post("/text")
async def text_data(text:text_model):
    text=text.text
    main.text(text=text)
    return{
        "response":" upload sussefuly"
    }


if __name__=="__main__":
    uvicorn.run(app=app,port=1200)
from fastapi import FastAPI,UploadFile,File

import uvicorn
from pydantic import BaseModel
from  fastapi.middleware.cors import CORSMiddleware
from typing import List


from src.main import Main
from src.components.ragchatbot import RagChatbot
from src.components.chatbot import Chatbot

app=FastAPI()

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
    return res
class get_url(BaseModel):
    url:str


class rag_url(BaseModel):
    question:str
    session_id=str

@app.post("/ragchatbot_url")
async def ragbot(user:rag_url):
    question=user.question
    session_is=user.session_id



if __name__=="__main__":
    uvicorn.run(app=app,port=1200)
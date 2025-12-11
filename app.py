from flask import Flask,request,Response,render_template,jsonify,send_file
import os 
from fastapi.responses import HTMLResponse,PlainTextResponse,FileResponse
from fastapi import FastAPI,UploadFile,File,Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn
import os


from main import Main


obj=Main()
Main()

# from fastapi import 

app=FastAPI()

UPLOAD_FOLDER = "uploaded_pdfs"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/",response_class=HTMLResponse)
def home():
    return FileResponse("templates/index.html")

@app.post("/for_link")
async def from_link(user_link:str=Form(...),question:str=Form(...)):
    
    try:
        response=obj.main_for_web(link=user_link,question=question)
        return PlainTextResponse(response)
    except Exception as e:
        print(e)
        return PlainTextResponse("Error preocessing link",status_code=500)
    
    
@app.post("/for_pdf")
async def from_pdf(pdf_file:UploadFile=File(...),question:str=Form(...)):
    try:
        save_path=os.path.join(UPLOAD_FOLDER,pdf_file.filename)
        response=obj.mian_for_pdf(pdf=save_path,question=question)
        return PlainTextResponse(response)
    except Exception as e:
        print(e)
        return PlainTextResponse("Erro during the processes",status_code=500)

# @app.post("for_text")
# async def from_text(text:str=Form(...),question:str=Form(...)):
#     try:
#         response=obj.mian_for_text(text_path=text)
    


if __name__=="__main__":
    uvicorn.run("main_api:app",host="0.0.0.0",port=1111,reload=True)






# @app.route("/")
# def home():
#     return render_template("index.html")

# @app.route("/for_link",methods=["POST","GET"])
# def from_link():
    
#     if request.method=="POST":
#         data=request.form.get("user_link")
#         try:
#             response=obj.main_for_web(link=data,question="what that repo is contain")
#             return response
#         except:
#             print("error")
#             return "error processing link",500

# @app.route("/for_pdf", methods=["POST"])
# def from_pdf():
#     if "pdf_file" not in request.files:
#         return "No file found in the request"

#     pdf = request.files["pdf_file"]

#     if pdf.filename == "":
#         return "No file selected"
#     save_path = os.path.join(UPLOAD_FOLDER, pdf.filename)
#     pdf.save(save_path)
#     try:
#         response = obj.mian_for_pdf(pdf=save_path,question="what is the softawre engineering")

#         return response

#     except Exception as e:
#         print("Error while processing PDF:", e)
#         return "Error processing PDF", 500


# #@app.route("/for")
    


# if __name__=="__main__":
#     app.run(host="0.0.0.0",port=1111,debug=True)
    
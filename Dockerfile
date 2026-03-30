FROM python:3.1 

WORKDIR /app

COPY  requirements.txt .

RUN pip install --no-cacahe-dir -r requirements.txt

RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')"

CMD [ "uvicorn","app:app","--host","0.0.0.0","--port","7860"]

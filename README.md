# AI Chatbot Platform (RAG + Normal Chatbot)

A **full-stack AI chatbot system** that supports both:

-  **Normal Chatbot (LLM-based)**
-  **RAG Chatbot (Website / PDF / Text-based Q&A)**

Built using **FastAPI + Next.js + FAISS + Sentence Transformers + Groq LLM**, and deployed on **Hugging Face Spaces (Backend)** and **Vercel (Frontend)**.

---

## 🌐 Live Demo

-  **Frontend (Vercel):**  
  https://chatbot-frontend-bice-nu.vercel.app/rag-chatbot  

-  **Backend API (Hugging Face):**  
  https://kirankumar29-chatbot.hf.space  

---

##  Features

###  Normal Chatbot
- Conversational AI (Groq LLM)
- Session-based chat
- ChatGPT-like UI

###  RAG Chatbot
-  Website-based Q&A  
-  PDF-based Q&A  
-  Text-based Q&A  
- Context-aware answers (no hallucination)
- FAISS vector search

###  Frontend UI
- Modern ChatGPT-style dark theme
- Sidebar navigation
- Separate Normal & RAG chatbot pages
- Upload + Chat workflow
- Real-time responses

---

##  How It Works (RAG Flow)

1. User uploads data (Website / PDF / Text)
2. Content is split into chunks
3. Embeddings are generated
4. Stored in FAISS vector database
5. User asks a question
6. Relevant chunks are retrieved
7. Groq LLM generates answer using context

---

##  Tech Stack

### 🔹 Backend
- FastAPI
- LangChain
- FAISS
- Sentence Transformers
- Groq API
- Qdrant

### 🔹 Frontend
- Next.js (React)
- Tailwind CSS
- shadcn/ui
- Axios

### 🔹 Deployment
- Hugging Face Spaces (Backend)
- Vercel (Frontend)

---

##  Project Structure

```bash
.
├── backend/
│   ├── app.py
│   ├── main.py
│   ├── requirements.txt
│   ├── uploads/
│   ├── embeddings/
│   └── src/
│       ├── components/
│       │   ├── chatbot.py
│       │   └── ragchatbot.py
│       ├── datatransformer/
│       └── utils/
│
│
├── Dockerfile
├── .env
└── README.md
```


## Installation  Setup & Run
🔹 Clone Repository
```
git clone https://github.com/kumar-kiran-24/chatbot
cd chatbot
pip install -r requirements.txt
uvicorn app:app --reload
```

## Environment Variables
```
.env

QDRANT_URL="qdrant url"
QDRANT_API_KEY="your api key"
HF_TOKEN="your api key"
GROQ_API_KEY="your api key"

```
## API Endpoints
- Endpoint	Description
- /chatbot	Normal chatbot
- /ragchatbot_url	RAG chatbot
- /upload-pdf	Upload PDF
- /web	Load website
- /text	Add raw text

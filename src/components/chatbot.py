import os 
from dotenv import load_dotenv
load_dotenv()

from langchain_groq import ChatGroq
from langchain_core.chat_history import BaseChatMessageHistory,InMemoryChatMessageHistory
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder



class Chatbot:
    def __init__(self):
        api_key=os.getenv("GROQ_API_KEY")
        self.llm=ChatGroq(model="llama-3.1-8b-instant",api_key=api_key)
        self.prompt=ChatPromptTemplate.from_messages([
            ("system", """You are an AI assistant.
            Give clear and helpful responses to the user."""),
            MessagesPlaceholder(variable_name="history"),
            ("human", "\n\nQuestion:\n{question}")
        ])

    def chat(self,question,session_id):
        session_store={}
        self.session_id = session_id 

        def get_session_history(session_id):
            if session_id not in session_store:
                session_store[session_id]=InMemoryChatMessageHistory()
            return session_store[session_id]
        
        chain=self.prompt|self.llm

        self.bot = RunnableWithMessageHistory(
        chain,
        get_session_history=get_session_history,
        input_messages_key="question",
        history_messages_key="history"
            )
        
        response=self.bot.invoke({"question":question},
                                    config={"configurable": {"session_id": session_id}})
        
        return response.content
        
if __name__=="__main__":
    obj=Chatbot()
    res=obj.chat(question="what is the ai",session_id="1")
    print(res)

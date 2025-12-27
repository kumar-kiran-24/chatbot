import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.chat_history import BaseChatMessageHistory, InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

class RagChatbot:
    store = {}          # stores chat history 
    context_store = {}  # stores context per session

    def __init__(self):
        self.llm = ChatGroq(
            model="llama-3.1-8b-instant",
            api_key=os.getenv("GROQ_API_KEY")
        )

    def ragchatbot(self, question, context, session_id):

        store = self.store
        context_store = self.context_store
        model = self.llm

       
        if session_id not in context_store:
            context_store[session_id] = context

       
        self.saved_context = context_store[session_id]
        self.session_id = session_id 

        def get_session_history(session_id: str) -> BaseChatMessageHistory:
            if session_id not in store:
                store[session_id] = InMemoryChatMessageHistory()
            return store[session_id]

        prompt = ChatPromptTemplate.from_messages([
            ("system", """
You are a context-based assistant.
Use ONLY the provided context and previous messages.
Never invent information.
If something is not in the context or chat history, say:
The information is not available in the provided context.
"""),
            MessagesPlaceholder(variable_name="history"),
            ("human", "Context:\n{context}\n\nQuestion:\n{question}")
        ])

        chain = prompt | model

        self.bot = RunnableWithMessageHistory(
            chain,
            get_session_history=get_session_history,
            input_messages_key="question",
            history_messages_key="history"
        )

       
        response = self.bot.invoke(
            {"question": question, "context": self.saved_context},
            config={"configurable": {"session_id": self.session_id}}
        )

        return response.content

    
    def ask(self, question):
        response = self.bot.invoke(
            {"question": question, "context": self.saved_context},
            config={"configurable": {"session_id": self.session_id}}
        )
        return response.content
    
    
    # def reset_session(self, session_id: int, reset_context: bool = True):
 
    #     if session_id in self.store:
    #         del self.store[session_id]

    #     if reset_context and session_id in self.context_store:
    #         del self.context_store[session_id]

    #     if hasattr(self, "session_id") and self.session_id == session_id:
    #         self.session_id = None
    #         self.saved_context = None
    #         self.bot = None

    #     return f"Session {session_id} reset successfully."


if __name__=="__main__":
    obj=RagChatbot()
    print(obj.ragchatbot(question="what is my name" ,context="my name is kiran kumar s i am genertaive ai engineer" ,session_id=1))
    print(obj.ask(question="what is my job"))
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_ollama import ChatOllama
from database import vectorstore
from operator import itemgetter

# Initialize LLM
llm = ChatOllama(model="llama3.2", temperature=0.1)

# In-memory session tracking
session_store = {}

def get_session_history(session_id: str):
    if session_id not in session_store:
        session_store[session_id] = ChatMessageHistory()
    return session_store[session_id]

# The medical grounded prompt template
contextual_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an advanced medical assistant. Answer using ONLY the provided context blocks. Cite the source page inline like (Page X).\n\nContext blocks:\n{context}"),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{question}"),
])

def format_docs_with_metadata(docs):
    formatted = []
    for doc in docs:
        page_num = doc.metadata.get("page", 0) + 1
        formatted.append(f"[Page {page_num}]:\n{doc.page_content}")
    return "\n\n".join(formatted)

def stream_rag_response(user_id: str, session_id: str, question: str):
    """Builds a dynamic context-filtered chain and streams the query."""
    secure_retriever = vectorstore.as_retriever(
        search_kwargs={"k": 4, "filter": {"user_id": user_id}}
    )
    
    rag_chain = (
        RunnablePassthrough.assign(
            context=(itemgetter("question") | secure_retriever | format_docs_with_metadata)
        )
        | contextual_prompt
        | llm
        | StrOutputParser()
    )
    
    conversational_chain = RunnableWithMessageHistory(
        rag_chain,
        get_session_history,
        input_messages_key="question",
        history_messages_key="chat_history",
    )
    
    # We change .invoke() to .stream()
    return conversational_chain.stream(
        {"question": question},
        config={"configurable": {"session_id": session_id}}
    )
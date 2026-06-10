from dotenv import load_dotenv
import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_groq import ChatGroq
from langchain_chroma import Chroma
from state import ResearchState
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import GoogleGenerativeAIEmbeddings

load_dotenv()

llm = ChatGroq(
    model = "llama-3.1-8b-instant"
)

def build_retrieve(pdf_path):
    loader = PyPDFLoader(pdf_path)
    document = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size= 500,
        chunk_overlap= 100
    )

    chunks = splitter.split_documents(document)

    embedding = GoogleGenerativeAIEmbeddings(
        model = "models/gemini-embedding-2"
    )

    if os.path.exists("chroma_db"):
        vectorstore = Chroma(
            persist_directory= "chroma_db",
            embedding_function= embedding

        )
    else:
        vectorstore = Chroma.from_documents(
            documents= chunks,
            embedding= embedding,
            persist_directory= "chroma_db"
        )

    retriever = vectorstore.as_retriever(search_type = "mmr", search_kwargs={"k": 3})
    return retriever

retriever = build_retrieve("Czech-travel-guide.pdf")

def pdf_research(state: ResearchState):
    question = state["question"]
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are given a question, Generate a hypothetical answer to the question: {question}")
    ])

    chain = prompt | llm | StrOutputParser()
    response = chain.invoke({
        "question": question
    })
    
    docs = retriever.invoke(response)
    content = "\n\n".join([doc.page_content for doc in docs])
    prompt1 = ChatPromptTemplate.from_messages([
        ("system", "You are an helpful AI assistant, you are given a content and you have to make the answer to the question using the given content: {content}"),
        ("human", "{question}")
    ])
    chain1 = prompt1 |llm | StrOutputParser()
    response1 = chain1.invoke({
        "content": content,
        "question": question
    })
    return {"pdf_research": [response1]}





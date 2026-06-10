from dotenv import load_dotenv
from state import ResearchState
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq

load_dotenv()

llm = ChatGroq(
    model = "llama-3.1-8b-instant"
)

def supervisor_node(state: ResearchState):
    question = state["question"]
    pdf_research = state["pdf_research"]
    web_research = state["web_research"]
    prompt = ChatPromptTemplate.from_messages([
    ("system", '''You are given a question, you have to decide whether we have to search the pdf or the web. Just say pdf or web as an answer.'''),
    ("human", "{question}")
])
    if pdf_research and web_research:
        return {"next_node": "FINISH"}
    else:
        chain = prompt | llm | StrOutputParser()
        response = chain.invoke({
    "question": question
})
        if response.lower().startswith("pdf"):
            return {"next_node": "pdf_research"}
        else:
            return {"next_node": "web_research"}


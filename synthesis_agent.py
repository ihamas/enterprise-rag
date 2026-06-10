from state import ResearchState
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

llm = ChatGroq(
    model = "llama-3.1-8b-instant"
)

def synthesis_node(state: ResearchState):
    pdf_research = state["pdf_research"]
    web_research = state["web_research"]
    question = state["question"]
    research = web_research + pdf_research
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You have been provide with the answers of the question and you have to look at the complete answer and make one final good top quality answer, answers: {answers}"),
        ("human", "{question}")
    ])
    chain = prompt | llm | StrOutputParser()
    response = chain.invoke({
        "answers": research,
        "question": question
    })
    return {"answer": response}
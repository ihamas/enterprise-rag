from dotenv import load_dotenv
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_groq import ChatGroq
from state import ResearchState
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

llm = ChatGroq(
    model = "llama-3.1-8b-instant"
)

tool = TavilySearchResults(max_results=3)

def web_research(state: ResearchState):
    question = state["question"]
    results = tool.invoke(question)
    content = "\n\n".join([r["content"] for r in results])
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an AI assistant and provided a research, use the research and write answer from it, research: {research}"),
        ("human", "{question}")
    ])
    chain = prompt | llm | StrOutputParser()
    response = chain.invoke({
        "research": content,
        "question": question
    })
    return {"web_research": [response]}

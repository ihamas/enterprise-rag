from typing import TypedDict, Annotated
import operator

class ResearchState(TypedDict):
    question: str
    pdf_research: Annotated[list[str], operator.add]
    web_research: Annotated[list[str], operator.add]
    next_node: str 
    answer: str


from pydantic import BaseModel
from fastapi import FastAPI
from graph import final_app

app = FastAPI()

class ResearchRequest(BaseModel):
    question: str

@app.post("/ask")
def ask(request: ResearchRequest):
    answer = final_app.invoke({
        "question": request.question
    })
    return {"answer": answer["answer"]}




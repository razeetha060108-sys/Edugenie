from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from qna import answer_question
from explanation_module import explain_topic
from quiz_module import generate_quiz
from summary_module import summarize_text
from learning_path import get_learning_recommendations


# Create FastAPI application
app = FastAPI(
    title="EduGenie",
    description="Google Gemini Powered Learning Assistant",
    version="1.0.0"
)


# Project folder location
BASE_DIR = Path(__file__).resolve().parent


# Static files
app.mount(
    "/static",
    StaticFiles(directory=str(BASE_DIR / "static")),
    name="static"
)


# HTML templates
templates = Jinja2Templates(
    directory=str(BASE_DIR / "templates")
)


# Request data format
class UserRequest(BaseModel):
    text: str


# Home page
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )


# Q&A
@app.post("/qa")
async def qa(request: UserRequest):

    result = answer_question(request.text)

    return {
        "result": result
    }


# Explanation
@app.post("/explain")
async def explain(request: UserRequest):

    result = explain_topic(request.text)

    return {
        "result": result
    }


# Quiz
@app.post("/quiz")
async def quiz(request: UserRequest):

    result = generate_quiz(request.text)

    return {
        "result": result
    }


# Summary
@app.post("/summarize")
async def summarize(request: UserRequest):

    result = summarize_text(request.text)

    return {
        "result": result
    }


# Learning path recommendation
@app.post("/learn/recommendations")
async def learning_recommendations(
    request: UserRequest
):

    result = get_learning_recommendations(
        request.text
    )

    return {
        "result": result
    }
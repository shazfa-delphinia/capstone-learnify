from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional
from ml.chatbot_pipeline import chatbot_pipeline

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QuizRequest(BaseModel):
    user_interest_answers: List[str]
    user_tech_answers_mcq: Dict[str, str]
    student_id: Optional[str] = None

@app.get("/")
def read_root():
    return {"message": "ML Pipeline API is running"}

@app.post("/predict")
async def predict_learning_path(request: QuizRequest):
    try:
        result = chatbot_pipeline(
            user_interest_answers=request.user_interest_answers,
            user_tech_answers_mcq=request.user_tech_answers_mcq,
            student_id=request.student_id
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


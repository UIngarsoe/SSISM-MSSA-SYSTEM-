# app.py
"""
MSSA Pyinnyashi System (V14) - FastAPI Backend Entry
Author: U Ingar Soe
Date: 2025
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from mssa_pyinnyashi import MSSAPredictor  # your core engine

app = FastAPI(
    title="MSSA Pyinnyashi System V14 API",
    description="Mobile Advisor and Strategic Companion Backend",
    version="0.1.0"
)

# Initialize MSSA engine
mssa_engine = MSSAPredictor()

# Example request model
class PredictRequest(BaseModel):
    name: str
    birth_date: str  # YYYY-MM-DD
    house_cycle: int

# Example response model
class PredictResponse(BaseModel):
    guidance: str
    probability_score: float

@app.get("/")
async def root():
    return {"message": "Welcome to MSSA Pyinnyashi System V14 API"}

@app.post("/predict", response_model=PredictResponse)
async def predict(request: PredictRequest):
    """
    Generate life journey guidance and probabilistic insights
    """
    try:
        result = mssa_engine.generate_guidance(
            name=request.name,
            birth_date=request.birth_date,
            house_cycle=request.house_cycle
        )
        return PredictResponse(
            guidance=result['guidance'],
            probability_score=result['score']
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)

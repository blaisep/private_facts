from fastapi import FastAPI
from pydantic import BaseModel, Field

# Define the heart rate model
# Warning, ChatGPT
class HeartRate(BaseModel):
    value: int = Field(..., title="Heart Rate", description="Heart rate in beats per minute (BPM)", ge=30, le=220)
    unit: str = Field("BPM", const=True, description="Heart rate unit")

# app = FastAPI()

# Route to receive heart rate data
# @app.post("/heart-rate/")
# async def record_heart_rate(heart_rate: HeartRate):
#     return {
#         "message": "Heart rate received successfully",
#         "heart_rate": heart_rate.value,
#         "unit": heart_rate.unit
#     }

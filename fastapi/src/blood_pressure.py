from pydantic import BaseModel, Field, validator
from fastapi import FastAPI, HTTPException
from typing import Optional

# app = FastAPI()

# Blood Pressure Pydantic Model


class BloodPressure(BaseModel):
    systolic: int = Field(..., ge=90, le=180, description="Systolic pressure in mmHg (should be between 90 and 180)")
    diastolic: int = Field(..., ge=60, le=120, description="Diastolic pressure in mmHg (should be between 60 and 120)")
    pulse: Optional[int] = Field(None, ge=40, le=180, description="Pulse rate in beats per minute (optional)")

    # Custom validator to check for a reasonable blood pressure range
    @validator("systolic", "diastolic")
    def check_blood_pressure_range(cls, value, values, field):
        if field.name == "systolic":
            if value < 90 or value > 180:
                raise ValueError("Systolic pressure must be between 90 and 180 mmHg.")
        elif field.name == "diastolic":
            if value < 60 or value > 120:
                raise ValueError("Diastolic pressure must be between 60 and 120 mmHg.")
        return value

    class Config:
        schema_extra = {
            "example": {
                "systolic": 120,
                "diastolic": 80,
                "pulse": 75
            }
        }

# Endpoint for Blood Pressure submission
@app.post("/blood-pressure/")
async def submit_blood_pressure(data: BloodPressure):
    return {"message": "Blood pressure data received successfully", "data": data}

# Example of endpoint to validate blood pressure values
@app.get("/validate-blood-pressure/")
async def validate_blood_pressure(systolic: int, diastolic: int, pulse: Optional[int] = None):
    # Validation is handled by Pydantic automatically when data is sent to the POST endpoint
    try:
        blood_pressure = BloodPressure(systolic=systolic, diastolic=diastolic, pulse=pulse)
        return {"message": "Valid blood pressure values", "data": blood_pressure}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


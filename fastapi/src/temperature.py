from fastapi import FastAPI
from pydantic import BaseModel, Field

# Define the temperature model in Kelvin
class Temperature(BaseModel):
    value: float = Field(..., title="Body Temperature", description="Body temperature in Kelvin", ge=0, le=1000)
    unit: str = Field("Kelvin", const=True, description="Temperature unit")

app = FastAPI()

# Route to receive temperature data
# @app.post("/temperature/")
# async def record_temperature(temp: Temperature):
#     return {"message": "Temperature received", "temperature": temp.value, "unit": temp.unit}

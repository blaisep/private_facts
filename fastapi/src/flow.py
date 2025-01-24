from pydantic import BaseModel, Field, conint
from fastapi import FastAPI, HTTPException

# app = FastAPI()

# FlowRate Pydantic Model
# Warning: ChatGPT
class FlowRate(BaseModel):
    flow_rate: conint(ge=0, le=10)  # Integer between 0 and 10

    class Config:
        schema_extra = {
            "example": {
                "flow_rate": 5
            }
        }

# Endpoint for FlowRate submission
# @app.post("/flow-rate/")
# async def submit_flow_rate(data: FlowRate):
#     return {"message": "Flow rate data received successfully", "data": data}
#
# # Example of endpoint to validate FlowRate value
# @app.get("/validate-flow-rate/")
# async def validate_flow_rate(flow_rate: int):
#     # Validation is handled by Pydantic automatically when data is sent to the POST endpoint
#     try:
#         flow_rate_obj = FlowRate(flow_rate=flow_rate)
#         return {"message": "Valid flow rate value", "data": flow_rate_obj}
#     except ValueError as e:
#         raise HTTPException(status_code=400, detail=str(e))

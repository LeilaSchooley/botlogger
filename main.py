from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

# This is a dummy API key for demonstration purposes.
# In a real-world scenario, you should securely manage and validate API keys.
API_KEY = "your_16_digit_api_key"


# Define the data model for JSON input
class DataItem(BaseModel):
    data: str


# Dependency function to check API key validity
def check_api_key(api_key: Optional[str] = None):
    if api_key is None or len(api_key) != 16 or api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")
    return api_key


# Endpoint to accept JSON data and save it to a text file
@app.post("/save_data/")
async def save_data(data_item: DataItem, api_key: str = Depends(check_api_key)):
    with open("data.txt", "a") as file:
        file.write(data_item.data + "\n")
    return {"message": "Data saved successfully!"}

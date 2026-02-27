from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from main import AMServiceAssistant

# 1. Initialize the FastAPI web server
app = FastAPI(
    title="AM Service AI - Routing & Retrieval API",
    description="Microservice to optimize and retrieve John Deere technical manuals.",
    version="1.0.0"
)

# 2. Load our master pipeline into memory
assistant = AMServiceAssistant()

# 3. Define the exact shape of the data we expect from the frontend
class QueryRequest(BaseModel):
    query: str

# 4. Create the POST endpoint
@app.post("/api/v1/search")
async def search_manuals(request: QueryRequest):
    """
    Receives a user query, routes intent, expands the query, and retrieves blocks.
    """
    try:
        # Pass the frontend's question directly into the pipeline we built!
        result = assistant.process_query(request.query)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
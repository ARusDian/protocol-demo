from fastapi import FastAPI
from pydantic import BaseModel
import time

# FastAPI app instance
app = FastAPI()


# Request model
class ChatRequest(BaseModel):
    username: str
    message: str


@app.post("/chat")
async def chat(request: ChatRequest):
    start_time = time.time()

    # Simple chatbot logic
    response_message = f"Hello {request.username}, you said: '{request.message}'"

    # Measure latency
    latency = (time.time() - start_time) * 1000  # in milliseconds

    return {"response": response_message, "latency": f"{latency:.2f} ms"}

@app.get("/ping")
async def ping():
    return "pong"


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8001)

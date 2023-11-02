import asyncio
import random

from starlette.responses import StreamingResponse
from fastapi import FastAPI
from sse_starlette.sse import EventSourceResponse

app = FastAPI()

# fastapi cors allow all

from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")
async def root():
    return {"message": "Hello World"}

def generate_event():
    ids = [1, 2]
    # get a random id
    id = random.choice(ids)
    return {
        # "id": id,
        # "event": "secondary-update-event",
        "data": {
            "id": id,
            "type": "secondary-saas",
            "message": "secondary saas signed"
        }
    }
@app.get("/stream/{id}")
async def stream(id: int):
    async def event_generator():
        for i in range(10):
            await asyncio.sleep(1.0)
            event = generate_event()
            # print(event, id)
            if event["data"]['id'] == id:
                yield event

    return EventSourceResponse(event_generator())
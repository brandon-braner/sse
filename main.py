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
        while True:

            """ 
            Imagine a pubsub message comes in here saying client id xyz 
            signed a docusign at location pdq
            """
            await asyncio.sleep(1.0)
            event = generate_event()
            event_id = event["data"]['id']
            print(event, event_id)
            if event_id == id:
                yield event

    return EventSourceResponse(event_generator())
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware


from api.core.database import init_db
from api.mail.controller import email_router
from api.sms.controller import sms_router
from api.subscriptions.controller import subscription_router


from api.utils.remove_422 import remove_422


app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(subscription_router)


@app.on_event("startup")
async def start_db():
    await init_db()


@app.get(path="/", summary="Index", tags=["Index"])
@remove_422
async def index():
    return JSONResponse(
        {
            "Framework": "FastAPI",
            "Message": "Subscribe to Mailing List!!",
        }
    )

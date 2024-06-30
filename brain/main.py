from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from prisma import Prisma
from services.ip_details import get_ip_details
from api.routes import api_endpoint
from starlette.datastructures import Headers
from fastapi.middleware.cors import CORSMiddleware


class NoCache(StaticFiles):
    def is_not_modified(
        self, response_headers: Headers, request_headers: Headers
    ):
        return False


app = FastAPI()
app.include_router(api_endpoint, prefix="/api")
app.mount("/assets", NoCache(directory="./static/"), name="assets")
app.mount("/attachments", NoCache(directory="./uploads/"), name="attachments")

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

prisma = Prisma(auto_register=True, connect_timeout=60000)


@app.on_event("startup")
async def startup() -> None:
    await prisma.connect()


@app.on_event("shutdown")
async def shutdown() -> None:
    if prisma.is_connected():
        await prisma.disconnect()


@app.get("/")
async def root():
    ip_details = await get_ip_details("185.65.135.253")
    print(ip_details)

    return {"title": "Looplens", "version": "1.0.0"}

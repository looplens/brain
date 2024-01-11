from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from prisma import Prisma
from helpers.get_ip_details import get_ip_details
from routes.routes import router as api_router
from starlette.datastructures import Headers

class NoCache(StaticFiles):
  def is_not_modified(self, response_headers: Headers, request_headers: Headers) -> bool:
    return False


app = FastAPI()
app.include_router(api_router, prefix="/api/v1")
app.mount("/assets", NoCache(directory="./assets/"), name="assets")

prisma = Prisma(
  auto_register=True,
  connect_timeout=60000
)


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

  return {
    "title": "Looplens",
    "version": "1.0.0"
  }

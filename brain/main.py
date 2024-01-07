from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from prisma import Prisma

from routes.users.routes import router as users_router
from routes.posts.routes import router as posts_router
from middlewares.json_control import json_middleware


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(users_router, prefix="/users")
app.include_router(posts_router, prefix="/posts")
# app.middleware("http")(json_middleware)
prisma = Prisma(auto_register=True)


@app.on_event("startup")
async def startup() -> None:
  await prisma.connect()


@app.on_event("shutdown")
async def shutdown() -> None:
  if prisma.is_connected():
    await prisma.disconnect()


@app.get("/")
async def root():
  return {
    "title": "Looplens",
    "version": "1.0.0"
  }


@app.get("/robots.txt")
async def robots():
  with open("./static/robots.txt", "r") as file:
    content = file.read()

  return HTMLResponse(content=content, status_code=200)

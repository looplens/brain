from argon2 import PasswordHasher
from fastapi import APIRouter, HTTPException, Request
from prisma.models import User


router = APIRouter()


@router.post("/login")
async def login(request: Request):
  try:
    data = await request.json()
  except ValueError:
    raise HTTPException(status_code=400, detail="Invalid JSON format")

  required_fields = ["username", "password"]
  missing_field = next((field for field in required_fields if data.get(field) is None), None)

  if missing_field:
    raise HTTPException(status_code=422, detail=f"{missing_field} is missing")

  user = await User.prisma().find_first(where={
    "username": data["username"]
  })

  if user:
    ph = PasswordHasher()

    try:
      if ph.verify(user.password, data["password"]):
        return { "status": True, "session": { "access_token": user.token } }
    except Exception as e:
      return { "status": False, "message": "The password does not match the supplied hash." }

  return { "status": False, "message": ":-)" }


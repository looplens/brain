from fastapi import APIRouter, HTTPException, Request
from prisma.models import User
from helpers.missing_data import missing_data


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
    return missing_data(f"{missing_field} eksik")

  user = await User.prisma().find_first(
    where={
      "username": data["username"],
      "password": data["password"]
    }
  )

  if user:
    return { "available": True, "session": { "token": user.token } }
  else:
    return { "available": False }


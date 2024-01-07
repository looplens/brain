from fastapi import APIRouter, HTTPException, Request
from prisma.models import User
from helpers.generate_token import generate_token
from helpers.missing_data import missing_data
from helpers.generate_verification_code import generate_verification_code


router = APIRouter()


@router.post("/register")
async def register(request: Request):
  try:
    data = await request.json()
  except ValueError:
    raise HTTPException(status_code=400, detail="Invalid JSON format")

  required_fields = ["name", "email", "username", "password", "password_control"]
  missing_field = next((field for field in required_fields if data.get(field) is None), None)

  if missing_field:
    return missing_data(f"{missing_field} eksik")

  if data["password"] != data["password_control"]:
    return missing_data("Şifreler eşleşmiyor")

  for field, db_field in [("username", "Bu kullanıcı adı kullanılıyor"), ("email", "Bu e-posta adresi kullanılıyor")]:
    check_count = await User.prisma().count(where={field: data.get(field)})

    if check_count != 0:
      return missing_data(db_field)


  verification_code = generate_verification_code()

  add_db = await User.prisma().create({
    "token": generate_token(),
    "name": data["name"],
    "username": data["username"],
    "email": data["email"],
    "password": data["password"],
    "avatar": "/static/avatar.png",
    "verify_code": verification_code,
    "accent_color": "#f7bf0a",
    "flags": 0
  })

  if add_db:
    return {"available": True, "user": { "token": add_db.token, "username": add_db.username }}
  else:
    return {"available": False}


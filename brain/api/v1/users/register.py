from fastapi import APIRouter, HTTPException, Request
from prisma.models import User
from services.id_generator import IDGenerator
from argon2 import PasswordHasher


router = APIRouter()
id_generator = IDGenerator()


@router.post("/register")
async def register(request: Request):
  try:
    data = await request.json()
  except ValueError:
    raise HTTPException(status_code=400, detail="Invalid JSON format")

  required_fields = ["name", "email", "username", "password", "password_control"]
  missing_field = next((field for field in required_fields if data.get(field) is None), None)

  if missing_field:
    raise HTTPException(status_code=422, detail=f"{missing_field} is missing")

  if data["password"] != data["password_control"]:
    raise HTTPException(status_code=422, detail=f"Şifreler eşleşmiyor")

  for field, db_field in [("username", "Bu kullanıcı adı kullanılıyor"), ("email", "Bu e-posta adresi kullanılıyor")]:
    check_count = await User.prisma().count(where={field: data.get(field)})

    if check_count != 0:
      raise HTTPException(status_code=422, detail=f"{db_field} is missing")


  verification_code = id_generator.six_digits()
  ph = PasswordHasher()

  hash = ph.hash(data["password"])

  add_db = await User.prisma().create({
    "token": id_generator.token(),
    "name": data["name"],
    "username": data["username"],
    "email": data["email"],
    "password": hash,
    "avatar": "/static/avatar.png",
    "verify_code": verification_code,
    "accent_color": "#f7bf0a",
    "flags": 0,
    "privacy_flags": 0,
    "points": 0,
  })

  if add_db:
    return {"available": True, "user": { "token": add_db.token, "username": add_db.username }}
  else:
    return {"available": False}


from fastapi import APIRouter, HTTPException, Request
from prisma.models import User
from services.id_generator import IDGenerator
from argon2 import PasswordHasher
from services.email_validator import is_valid_email
from services.process_request import process_request
import re


router = APIRouter()
id_generator = IDGenerator()
ph = PasswordHasher()


@router.post("/register")
async def register(request: Request):
    data = await process_request(request, ["name", "email", "username", "password", "password_control"])

    if data["password"] != data["password_control"]:
        return {"status": False, "message_code": 5}  # şifreler eşleşmiyor

    if not is_valid_email(data["email"]):
        return {"status": False, "message_code": 6}  # email arızalı

    if len(data["username"]) > 32 or len(data["username"]) < 2:
        return {"status": False, "message_code": 3}  # kullanıcı adı çok uzun

    if len(data["name"]) > 48:
        return {"status": False, "message_code": 2}  # isim çok uzun

    for field, db_field in [("username", "username"), ("email", "email")]:
        check_count = await User.prisma().count(where={field: data.get(field)})

        if check_count != 0:
            return {
                "status": False,
                "message_code": 4,
                "message": db_field,
            }  # x kullanılıyor

    verification_code = id_generator.six_digits()
    hashed_password = ph.hash(data["password"])
    safe_username = re.sub(r"[^a-zA-Z]", "", data["username"])

    add_db = await User.prisma().create(
        {
            "token": id_generator.token(),
            "name": data["name"],
            "username": safe_username.lower(),
            "email": data["email"],
            "password": hashed_password,
            "avatar": "assets/avatars/octopus-1.png",
            "verify_code": verification_code,
            "accent_color": "#f7bf0a",
            "flags": 0,
            "privacy_flags": 0,
            "points": 0,
        }
    )

    if add_db:
        return {
            "status": True,
            "user": add_db,
        }
    else:
        return {"status": False, "message_code": 1}

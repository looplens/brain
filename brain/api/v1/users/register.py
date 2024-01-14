import re
from fastapi import APIRouter, Request
from pydantic import BaseModel, EmailStr, constr, ValidationError
from prisma.models import User
from services.id_generator import IDGenerator
from argon2 import PasswordHasher
from services.email_validator import is_valid_email

router = APIRouter()
id_generator = IDGenerator()
ph = PasswordHasher()

class RegistrationData(BaseModel):
    name: constr(max_length=48)
    email: EmailStr
    username: constr(min_length=2, max_length=32)
    password: str
    password_control: str

ERROR_CODES = {
    "validation_error": 1,
    "username_in_use": 3,
    "email_in_use": 4,
    "password_mismatch": 5,
    "user_creation_failed": 6
}

@router.post("/register")
async def register(request: Request):
    try:
        data = await request.json()
        registration_data = RegistrationData(**data)
    except ValidationError:
        return {"status": False, "error_code": ERROR_CODES["validation_error"]}

    if registration_data.password != registration_data.password_control:
        return {"status": False, "error_code": ERROR_CODES["password_mismatch"]}

    existing_user_by_username = await User.prisma().find_first(where={"username": registration_data.username})
    if existing_user_by_username:
        return {"status": False, "error_code": ERROR_CODES["username_in_use"]}

    existing_user_by_email = await User.prisma().find_first(where={"email": registration_data.email})
    if existing_user_by_email:
        return {"status": False, "error_code": ERROR_CODES["email_in_use"]}

    user_token = id_generator.token()
    verification_code = id_generator.six_digits()
    hashed_password = ph.hash(registration_data.password)
    safe_username = re.sub(r"[^a-zA-Z]", "", registration_data.username)

    try:
        new_user = await User.prisma().create(
            data={
                "token": user_token,
                "name": registration_data.name,
                "email": registration_data.email,
                "username": safe_username,
                "password": hashed_password,
                "avatar": "assets/avatars/octopus-1.png",
                "verify_code": verification_code,
                "accent_color": "#f7bf0a",
                "flags": 0,
                "privacy_flags": 0,
                "points": 0,
            }
        )
    except Exception:
        return {"status": False, "error_code": ERROR_CODES["user_creation_failed"]}

    return {"status": True, "data": new_user}

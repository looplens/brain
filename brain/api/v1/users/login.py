from pydantic import BaseModel, constr
from argon2 import PasswordHasher
from fastapi import APIRouter, Request
from prisma.models import User

router = APIRouter()
ph = PasswordHasher()

class LoginData(BaseModel):
    username: constr(min_length=2, max_length=32)
    password: str

ERROR_CODES = {
    "user_not_found": 1,
    "password_mismatch": 2
}

@router.post("/login")
async def login(request: Request):
    try:
        data = await request.json()
        login_data = LoginData(**data)
    except ValueError as e:
        return {"status": False, "error_code": ERROR_CODES["validation_error"], "message": str(e)}

    print(login_data.username)

    user = await User.prisma().find_first(where={"username": login_data.username})

    if not user:
        return {"status": False, "error_code": ERROR_CODES["user_not_found"]}

    try:
        if ph.verify(user.password, login_data.password):
            return {"status": True, "data": {"access_token": user.token}}
    except Exception:
        return {"status": False, "error_code": ERROR_CODES["password_mismatch"]}

    return {"status": False, "error_code": "unknown_error"}

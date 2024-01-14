from argon2 import PasswordHasher
from fastapi import APIRouter, HTTPException, Request
from services.process_request import process_request
from prisma.models import User


router = APIRouter()


@router.post("/login")
async def login(request: Request):
    data = await process_request(request, ["username", "password"])

    user = await User.prisma().find_first(where={"username": data["username"]})

    if user:
        ph = PasswordHasher()

        try:
            if ph.verify(user.password, data["password"]):
                return {"status": True, "session": {"access_token": user.token}}
        except Exception as e:
            return {
                "status": False,
                "message": "The password does not match the supplied hash.",
            }

    return {"status": False, "message": ":-)"}

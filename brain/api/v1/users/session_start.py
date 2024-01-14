from argon2 import PasswordHasher
from fastapi import APIRouter, HTTPException, Request
from prisma.models import User
from services.process_request import process_request


router = APIRouter()


@router.post("/session_start")
async def session_start(request: Request):
    data = await process_request(request, ["token"])

    try:
        user = await User.prisma().find_first(where={"token": data["token"]})

        if user:
            return {"status": True, "user": user}
    except Exception as e:
        print("Kullanıcı gümledi")

    return {"status": False, "message": ":-)"}

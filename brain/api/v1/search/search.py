from fastapi import APIRouter, HTTPException, Request, Depends
from prisma.models import User, Block
from services.format_user import format_user
from services.flags import calculate_user_flags
from middleware.token import oauth2_token_control


router = APIRouter()


@router.get("/")
async def search(value: str | None = None, client = Depends(oauth2_token_control)):
  if value is not None:
    find_users = await User.prisma().find_many(
      where={
        "OR": [
          {"name": {"contains": value}},
          {"username": {"contains": value}},
        ]
      },
    )

    data = []

    for user in find_users:
      data.append({
        "type": "profile",
        "title": user.name,
        "subtitle": user.username,
        "image": user.avatar,
      })

    return {"status": True, "list": data}

  return {"status": False}

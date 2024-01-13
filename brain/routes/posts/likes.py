from typing import List
from fastapi import APIRouter, Depends, HTTPException, Request
from prisma.models import Post, Like, Comments, User
from prisma.enums import LikeType
from middlewares.token import oauth2_token_control
from helpers.format_user import format_user


router = APIRouter()


@router.get("/likes")
async def likes(request: Request, client = Depends(oauth2_token_control)):
  try:
    data = await request.json()
  except ValueError:
    raise HTTPException(status_code=400, detail="Invalid JSON format")

  required_fields = ["post_id", "type", "page"]
  missing_field = next((field for field in required_fields if field not in data), None)

  if missing_field:
    raise HTTPException(status_code=422, detail=f"{missing_field} is missing")

  post_id = data["post_id"]
  like_type = LikeType.POST if data["type"] == "POST" else LikeType.COMMENT
  page = int(data["page"])

  take_value = 30
  skip_value = 0 if page == 1 else page * take_value

  try:
    likes = await Like.prisma().find_many(
      take=take_value,
      skip=skip_value,
      where={
        "post_id": post_id,
        "type": like_type,
      },
      order={
        "created_at": "desc"
      }
    )

    return {
      "status": True,
      "list": [
        format_user(await User.prisma().find_first(where={
          "id": getattr(like, "user_id")
        }))
        for like in likes
      ],
      "page": page
    }
  except Exception as e:
    return {"status": False}

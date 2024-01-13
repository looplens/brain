from typing import List
from fastapi import APIRouter, Depends, HTTPException, Request
from prisma.models import Post, Like, Comments
from prisma.enums import LikeType
from middleware.token import oauth2_token_control


router = APIRouter()


@router.post("/like")
async def like(request: Request, client = Depends(oauth2_token_control)):
  try:
    data = await request.json()
  except ValueError:
    raise HTTPException(status_code=400, detail="Invalid JSON format")

  required_fields = ["post_id", "type"]
  missing_field = next((field for field in required_fields if field not in data), None)

  if missing_field:
    raise HTTPException(status_code=422, detail=f"{missing_field} is missing")

  post_id = data["post_id"]
  like_type = LikeType.POST if data["type"] == "POST" else LikeType.COMMENT

  if like_type == LikeType.POST:
    model = Post
  else:
    model = Comments

  post_control = await model.prisma().find_first(where={"id": post_id})

  if post_control:
    control_like = await Like.prisma().find_many(where={
       "user_id": client.id,
       "post_id": post_id,
       "type": like_type
    })

    if control_like:
      like = await Like.prisma().delete_many(where={
        "user_id": client.id,
        "post_id": post_id,
        "type": like_type
      })
    else:
      like = await Like.prisma().create(data={
        "user_id": client.id,
        "post_id": post_id,
        "type": like_type
      })

      if like:
        return {"status": True, "like": like}

  return {"status": False}

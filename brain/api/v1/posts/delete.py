from typing import List
from fastapi import APIRouter, Depends, HTTPException, Request
from prisma.models import Post, Like, Comments
from prisma.enums import LikeType
from services.flags import calculate_post_flags, PostFlags
from middleware.token import oauth2_token_control


router = APIRouter()


@router.delete("/")
async def delete_post(request: Request, client = Depends(oauth2_token_control)):
  try:
    data = await request.json()
  except ValueError:
    raise HTTPException(status_code=400, detail="Invalid JSON format")

  required_fields = ["post_id"]
  missing_field = next((field for field in required_fields if field not in data), None)

  if missing_field:
    raise HTTPException(status_code=422, detail=f"{missing_field} is missing")

  post_id = data["post_id"]

  post_control = await Post.prisma().find_first(where={
    "id": post_id,
    "author_id": client.id
  })

  if post_control:
    post_flags = calculate_post_flags(post_control.flags)

    if PostFlags.SELF_DELETED.name not in post_flags:
      delete_post = await Post.prisma().update(data={
        "flags": post_control.flags + PostFlags.SELF_DELETED.value + PostFlags.DISABLED_COMMENTS.value
      }, where={
        "id": post_id,
        "author_id": client.id
      })

      if delete_post:
        return {"status": True}

  return {"status": False}

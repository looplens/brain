from typing import List
from fastapi import APIRouter, Depends, HTTPException, Request
from prisma.models import Post, Bookmark
from middleware.token import oauth2_token_control


router = APIRouter()


@router.post("/add_bookmark")
async def add_bookmark(request: Request, client = Depends(oauth2_token_control)):
  try:
    data = await request.json()
  except ValueError:
    raise HTTPException(status_code=400, detail="Invalid JSON format")

  required_fields = ["post_id"]
  missing_field = next((field for field in required_fields if field not in data), None)

  if missing_field:
    raise HTTPException(status_code=422, detail=f"{missing_field} is missing")

  post_id = data["post_id"]

  post_control = await Post.prisma().find_first(where={"id": post_id})

  if post_control:
    control_bookmark = await Bookmark.prisma().find_many(where={
       "author_id": client.id,
       "post_id": post_id
    })

    if control_bookmark:
      bookmark = await Bookmark.prisma().delete_many(where={
        "author_id": client.id,
        "post_id": post_id
      })
    else:
      bookmark = await Bookmark.prisma().create(data={
        "author_id": client.id,
        "post_id": post_id
      })

      if bookmark:
        return {"status": True, "like": bookmark}

  return {"status": False}

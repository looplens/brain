from typing import List
from fastapi import APIRouter, Depends, HTTPException, Request
from prisma.models import Post, Comments, User, Like
from prisma.enums import CommentType, LikeType
from helpers.format_user import format_user
from middlewares.token import oauth2_token_control
from helpers.flags import calculate_comment_flags, calculate_post_flags, PostFlags, CommentFlags


router = APIRouter()


@router.get("/")
async def comments(request: Request, client = Depends(oauth2_token_control)):
  try:
    data = await request.json()
  except ValueError:
    raise HTTPException(status_code=400, detail="Invalid JSON format")

  required_fields = ["post_id", "page"]
  missing_field = next((field for field in required_fields if field not in data), None)

  if missing_field:
    raise HTTPException(status_code=422, detail=f"{missing_field} is missing")

  page = int(data["page"])

  take_value = 30
  skip_value = 0 if page == 1 else page * take_value

  list = []

  try:
    get_comments = await Comments.prisma().find_many(
      take=take_value,
      skip=skip_value,
      where={"post_id": data["post_id"]},
      order={"created_at": "desc"}
    )

    for comment in get_comments:
      comment_flags = calculate_comment_flags(comment.flags)

      if CommentFlags.SELF_DELETED.name not in comment_flags and CommentFlags.SYSTEM_DELETED.name not in comment_flags:
        comment_author = await User.prisma().find_first(where={"id": comment.author_id})
        comment_likes = await Like.prisma().count(where={
          "post_id": data["post_id"],
          "type": LikeType.COMMENT
        })
        is_liked = await Like.prisma().find_first(where={
          "post_id": data["post_id"],
          "user_id": client.id
        })
        reply_count = await Comments.prisma().count(where={
          "replied_to": comment.id
        })

        list.append({
          "id": comment.id,
          "author": format_user(comment_author),

          "content": comment.content,

          "react_count": comment_likes,
          "is_liked": True if is_liked else False,

          "post_id": comment.post_id,

          "replied_to": comment.replied_to,
          "reply_count": reply_count,

          "flags": comment.flags,
          "created_at": comment.created_at,
          "updated_at": comment.updated_at
        })
  except Exception as e:
    print("Yorumlarda bi' sorun meydana geldi")

  return {"status": True, "comments": list, "page": page}


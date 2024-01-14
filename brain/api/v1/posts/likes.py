from typing import List
from fastapi import APIRouter, Depends, HTTPException, Request
from prisma.models import Post, Like, Comments, User
from prisma.enums import LikeType
from middleware.token import oauth2_token_control
from services.format_user import format_user
from services.process_request import process_request


router = APIRouter()


@router.get("/likes")
async def likes(request: Request, client=Depends(oauth2_token_control)):
    data = await process_request(request, ["post_id", "type", "page"])

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
            order={"created_at": "desc"},
        )

        return {
            "status": True,
            "list": [
                format_user(
                    await User.prisma().find_first(
                        where={"id": getattr(like, "user_id")}
                    )
                )
                for like in likes
            ],
            "page": page,
        }
    except Exception as e:
        return {"status": False}

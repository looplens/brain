from typing import List
from fastapi import APIRouter, Depends, HTTPException, Request
from prisma.models import Post, Like, Comments
from prisma.enums import LikeType
from services.flags import calculate_post_flags, PostFlags
from middleware.token import oauth2_token_control
from services.process_request import process_request


router = APIRouter()


@router.delete("/")
async def delete_post(request: Request, client=Depends(oauth2_token_control)):
    data = await process_request(request, ["post_id"])

    post_id = data["post_id"]

    post_control = await Post.prisma().find_first(
        where={"id": post_id, "author_id": client.id}
    )

    if post_control:
        post_flags = calculate_post_flags(post_control.flags)

        if PostFlags.SELF_DELETED.name not in post_flags:
            delete_post = await Post.prisma().update(
                data={
                    "flags": post_control.flags
                    + PostFlags.SELF_DELETED.value
                    + PostFlags.DISABLED_COMMENTS.value
                },
                where={"id": post_id, "author_id": client.id},
            )

            if delete_post:
                return {"status": True}

    return {"status": False}

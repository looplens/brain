from typing import List
from fastapi import APIRouter, Depends, HTTPException, Request
from prisma.models import Post, Comments
from prisma.enums import CommentType
from middleware.token import oauth2_token_control
from services.process_request import process_request
from services.flags import (
    calculate_comment_flags,
    calculate_post_flags,
    PostFlags,
    CommentFlags,
)


router = APIRouter()


@router.delete("/")
async def delete(request: Request, client=Depends(oauth2_token_control)):
    data = await process_request(request, ["post_id"])

    comment_control = await Comments.prisma().find_first(
        where={
            "id": data["comment_id"],
        }
    )

    if comment_control:
        continue_delete = False
        comment_flags = calculate_comment_flags(comment_control.flags)

        if comment_control.author_id == client.id:
            continue_delete = CommentFlags.SELF_DELETED.value
        else:
            post_control = await Post.prisma().find_first(
                where={"id": comment_control.post_id}
            )

            if post_control and post_control.author_id == client.id:
                continue_delete = CommentFlags.POST_AUTHOR_DELETE.value

        if continue_delete is not False:
            if (
                CommentFlags.SELF_DELETED.name not in comment_flags
                and CommentFlags.POST_AUTHOR_DELETE.name not in comment_flags
            ):
                try:
                    delete_comment = await Comments.prisma().update(
                        data={"flags": comment_control.flags + continue_delete},
                        where={"id": data["comment_id"]},
                    )
                except Exception as e:
                    raise HTTPException(
                        status_code=500, detail="Error deleting comment."
                    )

                if delete_comment:
                    return {"status": True}

    return {"status": False}

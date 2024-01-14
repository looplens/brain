from typing import List
from fastapi import APIRouter, Depends, HTTPException, Request
from prisma.models import Post, Comments
from prisma.enums import CommentType
from middleware.token import oauth2_token_control
from services.flags import calculate_comment_flags, calculate_post_flags, PostFlags
from services.process_request import process_request


router = APIRouter()


@router.put("/")
async def new_comment(request: Request, client=Depends(oauth2_token_control)):
    data = await process_request(request, ["post_id", "replied_to", "content", "type"])

    content = data["content"]
    comment_type = (
        CommentType.COMMENT if data["type"] == "COMMENT" else CommentType.REPLY
    )

    if len(content) <= 128:
        post_control = await Post.prisma().find_first(where={"id": data["post_id"]})
        post_flags = calculate_post_flags(post_control.flags)

        if post_control and PostFlags.DISABLED_COMMENTS.name not in post_flags:
            replied_controlled_id = None

            if comment_type == CommentType.REPLY:
                reply_control = await Comments.prisma().find_first(
                    where={"id": data["replied_to"], "post_id": data["post_id"]}
                )

                if reply_control:
                    replied_controlled_id = reply_control.id
                else:
                    comment_type = CommentType.COMMENT

            create_comment = await Comments.prisma().create(
                data={
                    "author_id": client.id,
                    "post_id": post_control.id,
                    "replied_to": replied_controlled_id,
                    "content": content,
                    "flags": 0,
                    "type": comment_type,
                }
            )

            if create_comment:
                return {"status": True, "comment_id": create_comment.id}

    return {"status": False}

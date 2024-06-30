from typing import List
from fastapi import APIRouter, Depends, HTTPException, Request
from prisma.models import Post, Like, Comments, Follow, User, Bookmark
from prisma.enums import LikeType
from services.flags import calculate_post_flags, PostFlags
from services.format_user import format_user
from middleware.token import oauth2_token_control
from services.process_request import process_request
import re

router = APIRouter()


@router.post("/collect")
async def get_posts(request: Request, client=Depends(oauth2_token_control)):
    data = await process_request(request, ["type", "term", "page"])

    page = int(data["page"])
    take_value = 30
    skip_value = 0 if page == 1 else page * take_value
    posts = None

    try:
        match data["type"]:
            case "profile":
                get_user = await User.prisma().find_first(
                    where={"username": data["term"]}
                )

                if get_user:
                    posts = await Post.prisma().find_many(
                        take=take_value,
                        skip=skip_value,
                        where={"author_id": get_user.id},
                        order={"created_at": "desc"},
                    )

            case "feed":
                feed_user_ids = [client.id]
                followings = await Follow.prisma().find_many(
                    where={"client_id": client.id, "type": "ACCEPT"}
                )

                for following in followings:
                    feed_user_ids.append(following.profile_id)

                posts = await Post.prisma().find_many(
                    take=take_value,
                    skip=skip_value,
                    where={"author_id": {"in": feed_user_ids}},
                    order={"created_at": "desc"},
                )
    except Exception as e:
        return {"status": False, "message": "Something went wrong during pairing."}

    response_array = []

    try:
        for post in posts:
            post_flags = calculate_post_flags(post.flags)

            if (
                PostFlags.SELF_DELETED.name not in post_flags
                and PostFlags.SYSTEM_DELETED.name not in post_flags
            ):
                publisher = await User.prisma().find_first(where={"id": post.author_id})

                if publisher:
                    is_liked = await Like.prisma().find_first(
                        where={"post_id": post.id, "user_id": client.id}
                    )
                    is_saved = await Bookmark.prisma().find_first(
                        where={"post_id": post.id, "author_id": client.id}
                    )

                    response_array.append(
                        {
                            "id": post.id,
                            "published": format_user(publisher),
                            "is_loop": False,
                            "full_text": post.content,
                            "text_range": [0, len(post.content)],
                            "created_at": post.created_at,
                            "updated_at": post.updated_at,
                            "coordinates": None,
                            "place": post.location,
                            "flags": post.flags,
                            "media_attachments": post.attachments.split(","),
                            "is_liked": True if is_liked else False,
                            "is_saved": True if is_saved else False,
                            "tags": re.findall(r"#\w+", post.content),
                            "poll": None,
                            "visibility": "public",
                        }
                    )
    except Exception as e:
        return {"status": False, "message": "An error occurred while processing posts."}

    return {"status": True, "posts": response_array}

from fastapi import APIRouter, Depends
from prisma.models import User, Follow
from middleware.token import oauth2_token_control


router = APIRouter()


@router.get("/profile")
async def profile(username: str | None = None, client = Depends(oauth2_token_control)):
  result = {"available": False}

  if username is not None:
    user = await User.prisma().find_first(where={"username": username})

    if user:
      followers = await Follow.prisma().count(where={"profile_id": user.id, "type": "ACCEPT"})
      followings = await Follow.prisma().count(where={"client_id": user.id, "type": "ACCEPT"})

      result["available"] = True
      result["profile"] = {
        "id": user.id,
        "name": user.name,
        "username": user.username,
        "avatar": user.avatar,
        "accent_color": user.accent_color,
        "about": user.about,
        "website": user.website,
        "flags": user.flags,
        "joined_at": user.created_at,
      }
      result["metrics"] = {
        "followers": followers,
        "followings": followings,
        "posts": 0,
      }

  return result

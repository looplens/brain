from fastapi import APIRouter, HTTPException, Request, Depends
from prisma.models import User, Follow
from prisma.enums import FollowType
from helpers.format_user import format_user
from middlewares.token import oauth2_token_control


router = APIRouter()


@router.post("/follow")
async def follow(request: Request, client = Depends(oauth2_token_control)):
  try:
    data = await request.json()
  except ValueError:
    raise HTTPException(status_code=400, detail="Invalid JSON format")

  required_fields = ["profile_id"]
  missing_field = next((field for field in required_fields if field not in data), None)

  if missing_field:
    raise HTTPException(status_code=422, detail=f"{missing_field} is missing")

  if data["profile_id"] == client.id:
    raise HTTPException(status_code=422, detail=f"You cant follow your profile!")

  user = await User.prisma().find_first(where={"id": data["profile_id"]})

  if user:
    follow_instance = await Follow.prisma().find_first(
      where={
        "client_id": client.id,
        "profile_id": data["profile_id"]
      }
    )

    if follow_instance:
      await Follow.prisma().delete_many(
        where={
            "client_id": client.id,
            "profile_id": data["profile_id"]
        }
      )

      message = "unfollow"
    else:
      await Follow.prisma().create(
        data={
          "client_id": client.id,
          "profile_id": data["profile_id"],
          "type": FollowType.ACCEPT
        }
      )

      message = "follow"

    return {"status": True, "message": message}
  else:
    return {"status": False, "message": "no user"}


async def get_follow_data(username: str, profile_id_field: str, endpoint: str):
  result = {"available": False, "list": []}

  if username is not None:
    user = await User.prisma().find_first(where={"username": username})

    if user:
      follow_data = await Follow.prisma().find_many(where={
        profile_id_field: user.id,
        type: FollowType.ACCEPT
      })

      result["status"] = True
      result["list"] = [
        format_user(await User.prisma().find_first(where={"id": getattr(f, 'client_id' if endpoint == 'followers' else 'profile_id')}))
        for f in follow_data
      ]

  return result


@router.get("/followers")
async def followers(username: str | None = None, client = Depends(oauth2_token_control)):
  return await get_follow_data(username, "profile_id", "followers")


@router.get("/followings")
async def followings(username: str | None = None, client = Depends(oauth2_token_control)):
  return await get_follow_data(username, "client_id", "followings")


@router.get("/requests")
async def requests(client = Depends(oauth2_token_control)):
  pending_requests = await Follow.prisma().find_many(where={
    "profile_id": client.id,
    "type": FollowType.PENDING
  })

  return {
    "status": True,
    "requests": [
      {
        "user": format_user(await User.prisma().find_first(where={
          "id": getattr(preq, "profile_id")
        })),
        "created_at": preq.created_at,
        "updated_at": preq.updated_at
      }
      for preq in pending_requests
    ]
  }

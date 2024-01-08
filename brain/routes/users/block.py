from fastapi import APIRouter, HTTPException, Request, Depends
from prisma.models import User, Block
from helpers.format_user import format_user
from middlewares.token import oauth2_token_control


router = APIRouter()


@router.post("/block")
async def block(request: Request, client = Depends(oauth2_token_control)):
  try:
    data = await request.json()
  except ValueError:
    raise HTTPException(status_code=400, detail="Invalid JSON format")

  required_fields = ["profile_id"]
  missing_field = next((field for field in required_fields if field not in data), None)

  if missing_field:
    raise HTTPException(status_code=422, detail=f"{missing_field} is missing")

  if data["profile_id"] == client.id:
    raise HTTPException(status_code=422, detail=f"You cant block yourself.")

  user = await User.prisma().find_first(where={"id": data["profile_id"]})

  if user:
    block_instance = await Block.prisma().find_first(
      where={
        "client_id": client.id,
        "user_id": data["profile_id"]
      }
    )

    if block_instance:
      await Block.prisma().delete_many(
        where={
            "client_id": client.id,
            "user_id": data["profile_id"]
        }
      )

      status = "unblock"
    else:
      await Block.prisma().create(
        data={
          "client_id": client.id,
          "user_id": data["profile_id"]
        }
      )

      status = "block"

    return {"available": True, "status": status}
  else:
    return {"available": False, "status": "no user"}


@router.get("/blocks")
async def blocks(id: str | None = None):
  result = {"available": False, "list": []}

  if id is not None:
    users = await Block.prisma().find_many(where={
      "client_id": id
    })

    result["available"] = True
    result["list"] = [
      format_user(await User.prisma().find_first(where={"id": f.user_id}))
      for f in users
    ]

  return result

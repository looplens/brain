from fastapi import APIRouter, HTTPException, Request, Depends
from prisma.models import User, Block
from services.format_user import format_user
from middleware.token import oauth2_token_control
from services.process_request import process_request


router = APIRouter()


@router.post("/block")
async def block(request: Request, client=Depends(oauth2_token_control)):
    data = await process_request(request, ["profile_id"])

    if data["profile_id"] == client.id:
        raise HTTPException(status_code=422, detail=f"You cant block yourself.")

    user = await User.prisma().find_first(where={"id": data["profile_id"]})

    if user:
        block_instance = await Block.prisma().find_first(
            where={"client_id": client.id, "user_id": data["profile_id"]}
        )

        if block_instance:
            await Block.prisma().delete_many(
                where={"client_id": client.id, "user_id": data["profile_id"]}
            )

            status = "unblock"
        else:
            await Block.prisma().create(
                data={"client_id": client.id, "user_id": data["profile_id"]}
            )

            status = "block"

        return {"available": True, "status": status}
    else:
        return {"available": False, "status": "no user"}


@router.get("/blocks")
async def blocks(id: str | None = None, client=Depends(oauth2_token_control)):
    result = {"available": False, "list": []}

    if id is not None:
        users = await Block.prisma().find_many(where={"client_id": id})

        result["available"] = True
        result["list"] = [
            format_user(await User.prisma().find_first(where={"id": f.user_id}))
            for f in users
        ]

    return result

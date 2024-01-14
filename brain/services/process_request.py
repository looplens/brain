from fastapi import APIRouter, HTTPException, Request


async def process_request(request: Request, required_fields):
    try:
        data = await request.json()
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid JSON format")

    missing_field = next(
        (field for field in required_fields if data.get(field) is None), None
    )

    if missing_field:
        raise HTTPException(status_code=422, detail=f"{missing_field} is missing")

    return data

from fastapi import Request
from fastapi.responses import JSONResponse


async def json_middleware(request: Request, call_next):
  try:
    data = await request.json()
  except ValueError:
    return JSONResponse(content={"error": "Geçersiz JSON biçimi"}, status_code=400)

  if not data:
    return JSONResponse(content={"error": "JSON boş"}, status_code=400)

  response = await call_next(request)
  return response

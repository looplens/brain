from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from prisma.models import User


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def oauth2_token_control(token: str = Depends(oauth2_scheme)):
  control = await User.prisma().find_first(
    where={"token": token}
  )

  if not control:
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Invalid credentials",
      headers={"WWW-Authenticate": "Bearer"},
    )

  return control

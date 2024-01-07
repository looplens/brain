import secrets

def generate_token(length = 48):
  token = secrets.token_hex(length // 2)
  return token

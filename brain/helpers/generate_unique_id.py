import secrets

def generate_unique_id(length = 32):
  unique_id = secrets.token_hex(length // 2)
  return unique_id

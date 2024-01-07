import random

def generate_verification_code():
  return "".join(random.choice('0123456789') for _ in range(6))

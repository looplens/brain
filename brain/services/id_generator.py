import time
import secrets
import random
from snowflake import SnowflakeGenerator

class IDGenerator:
  def __init__(self, snowflake_seed=42):
    self.snowflake_generator = SnowflakeGenerator(snowflake_seed)

  def snowflake(self):
    return next(self.snowflake_generator)

  def token(self, length=48):
    return secrets.token_hex(length // 2)

  def unique_id(self, length=32):
    return secrets.token_hex(length // 2)

  def six_digits(self):
    return "".join(random.choice('0123456789') for _ in range(6))

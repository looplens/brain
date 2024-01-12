import time
from snowflake import SnowflakeGenerator

async def generate_snowflake():
  snowflake = SnowflakeGenerator(42)
  return next(snowflake)

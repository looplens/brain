from snowflake import SnowflakeGenerator

def generate_snowflake():
  snowflake = SnowflakeGenerator(42)
  return next(snowflake)

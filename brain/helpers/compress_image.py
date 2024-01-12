from PIL import Image
import io

async def compress_image(content: bytes) -> bytes:
  image = Image.open(io.BytesIO(content))

  compressed_image = io.BytesIO()
  image.save(compressed_image, format="JPEG", quality=40)

  return compressed_image.getvalue()

from typing import List
from fastapi import APIRouter, Depends, File, UploadFile, Form
from prisma.models import Post
from helpers.compress_image import compress_image
from helpers.compress_video import compress_video
from helpers.generate_unique_id import generate_unique_id
from middlewares.token import oauth2_token_control
import os


router = APIRouter()


@router.put("/")
async def create_post(
  content: str = Form(default=None),
  location: str = Form(default=None),
  files: list[UploadFile] = File(default=None),
  client = Depends(oauth2_token_control)
):
  max_file_size = 24 * 1024 * 1024
  base_folder = "./uploads"
  uploaded_attachments = []

  if not os.path.exists(base_folder):
    os.makedirs(base_folder)

  if content is not None or files is not None:
    try:
      for uploaded_file in files:
        if uploaded_file.file and uploaded_file.file.__sizeof__() > max_file_size:
          return {"status": False, "message": f"File size exceeds the limit (maximum {max_file_size}MB)"}
    except Exception as e:
      return {"status": False, "message": f"An error occurred while parsing the files"}

    try:
      post = await Post.prisma().create(data={
        "author_id": client.id,
        "content": content,
        "attachments": "",
        "location": location,
        "flags": 0,
      })
    except Exception as e:
      return {"status": False, "message": f"An error occurred while creating a post"}

    if files is not None:
      try:
        for uploaded_file in files:
          post_folder = f"{base_folder}/{client.id}/{post.id}"

          if not os.path.exists(post_folder):
            os.makedirs(post_folder)

          _, file_extension = os.path.splitext(uploaded_file.filename)
          file_name_original   = f"{post_folder}/xl_{generate_unique_id()}{file_extension.lower()}"
          file_name_compressed = f"{post_folder}/xs_{generate_unique_id()}{file_extension.lower()}"
          file_content = await uploaded_file.read()

          if file_extension.lower() in {".jpg", ".jpeg", ".png"}:
            compressed_content = await compress_image(file_content)

            with open(file_name_compressed, "wb") as new_file:
              new_file.write(compressed_content)

            with open(file_name_original, "wb") as new_file:
              new_file.write(file_content)

            uploaded_attachments.append(file_name_compressed.replace(base_folder, "attachments"))
          elif file_extension.lower() in {".mp4", ".avi", ".mkv", ".mov"}:
            with open(file_name_original, "wb") as new_file:
              new_file.write(file_content)

            compressed_video = compress_video(file_name_original, file_name_compressed)

            if compressed_video:
              uploaded_attachments.append(file_name_compressed.replace(base_folder, "attachments"))
            else:
              uploaded_attachments.append(file_name_original.replace(base_folder, "attachments"))
      except Exception as e:
        return {"status": False, "message": "An error occurred while saving content"}

      if uploaded_attachments:
        try:
          post = await Post.prisma().update(
            where={"id": post.id},
            data={"attachments": ",".join(uploaded_attachments)}
          )

          return {"status": True, "post": post}
        except Exception as e:
          return {"status": False, "message": f"An error occurred while updating a post"}

  return {"status": False, "message": "Post content is missing"}

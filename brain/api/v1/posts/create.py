from typing import List
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, Form
from pydantic import BaseModel
from prisma.models import Post
from services.id_generator import IDGenerator
from services.compressor import MediaCompressor
from middleware.token import oauth2_token_control
import os

router = APIRouter()
id_generator = IDGenerator()
media_compressor = MediaCompressor()

ERROR_CODES = {
    "file_size_exceeded": 1,
    "post_creation_failed": 2,
    "file_parsing_error": 3,
    "file_saving_error": 4,
    "post_update_failed": 5,
    "missing_content": 6
}

@router.put("/")
async def create_post(
    content: str = Form(default=None),
    location: str = Form(default=None),
    files: List[UploadFile] = File(default=None),
    client=Depends(oauth2_token_control),
):
    max_file_size = 24 * 1024 * 1024
    base_folder = "./uploads"
    uploaded_attachments = []

    if not os.path.exists(base_folder):
        os.makedirs(base_folder)

    if content is None and not files:
        return {"status": False, "error_code": ERROR_CODES["missing_content"]}

    if files is not None:
        for uploaded_file in files:
            if uploaded_file.file.__sizeof__() > max_file_size:
                return {"status": False, "error_code": ERROR_CODES["file_size_exceeded"]}

    try:
        post = await Post.prisma().create(
            data={
                "author_id": client.id,
                "content": content,
                "attachments": "",
                "location": location,
                "flags": 0,
            }
        )
    except Exception as e:
        return {"status": False, "error_code": ERROR_CODES["post_creation_failed"]}

    if files is not None:
        try:
            for uploaded_file in files:
                post_folder = f"{base_folder}/{client.id}/{post.id}"

                if not os.path.exists(post_folder):
                    os.makedirs(post_folder)

                _, file_extension = os.path.splitext(uploaded_file.filename)
                file_unique_id = id_generator.unique_id()
                file_name_original = (
                    f"{post_folder}/xl_{file_unique_id}{file_extension.lower()}"
                )
                file_name_compressed = (
                    f"{post_folder}/xs_{file_unique_id}{file_extension.lower()}"
                )
                file_content = await uploaded_file.read()

                if file_extension.lower() in {".jpg", ".jpeg", ".png"}:
                    compressed_content = await media_compressor.compress_image(
                        file_content
                    )

                    with open(file_name_compressed, "wb") as new_file:
                        new_file.write(compressed_content)

                    with open(file_name_original, "wb") as new_file:
                        new_file.write(file_content)

                    uploaded_attachments.append(
                        file_name_compressed.replace(base_folder, "attachments")
                    )
                elif file_extension.lower() in {".mp4", ".avi", ".mkv", ".mov"}:
                    with open(file_name_original, "wb") as new_file:
                        new_file.write(file_content)

                    compressed_video = media_compressor.compress_video(
                        file_name_original, file_name_compressed
                    )

                    if compressed_video:
                        uploaded_attachments.append(
                            file_name_compressed.replace(base_folder, "attachments")
                        )
                    else:
                        uploaded_attachments.append(
                            file_name_original.replace(base_folder, "attachments")
                        )

        except Exception as e:
            return {"status": False, "error_code": ERROR_CODES["file_saving_error"]}

    if uploaded_attachments:
        try:
            post = await Post.prisma().update(
                where={"id": post.id},
                data={"attachments": ",".join(uploaded_attachments)},
            )
        except Exception as e:
            return {"status": False, "error_code": ERROR_CODES["post_update_failed"]}

    return {"status": True, "post": post}

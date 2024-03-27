import logging
import os
from pathlib import Path
from io import BytesIO
import aiofiles  # type: ignore
import secrets

from fastapi import UploadFile
from PIL import Image  # type: ignore

logger = logging.getLogger(__name__)


def check_fastapi_request_uploaded_image_valid(image: UploadFile):
    if image.content_type and image.content_type.startswith(
            "image/") and image.filename:
        file_extension = image.filename.split('.')[-1]
        if file_extension.lower() in ['png', 'jpeg', 'jpg']:
            try:
                img = Image.open(BytesIO(image.file.read()))
                img.verify()
                return True
            except Exception as e:
                logger.error("Error opening image file with Pillow:")
                logger.error(e)
            finally:
                image.file.seek(0)
    return False


def generate_safe_image_file_name(file_extension=""):
    filename = secrets.token_urlsafe(32)
    if file_extension:
        return f"{filename}.{file_extension}"
    return filename


async def save_image_to_uploads(image: UploadFile):
    if not image.filename:
        raise Exception(
            'Could not determine file extension as image.filename is None')
    file_extension = image.filename.split('.')[-1].lower()
    filename = generate_safe_image_file_name(file_extension=file_extension)
    filepath = Path(os.getcwd()).parent.joinpath("image_uploads", filename)
    image.file.seek(0)
    async with aiofiles.open(filepath, 'wb') as out_file:
        await out_file.write(await image.read())
    return f"/uploads/{filename}"


def delete_image(image_url: str):
    filename = image_url.split("/uploads/")[1]
    filepath = Path(os.getcwd()).parent.joinpath("image_uploads", filename)
    try:
        os.remove(filepath)
    except OSError:
        pass

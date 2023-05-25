import hashlib

import cloudinary
import cloudinary.uploader

from src.conf.config import settings


class UploadService:
    cloudinary.config(
        cloud_name=settings.cloudinary_name,
        api_key=settings.cloudinary_apy_key,
        api_secret=settings.cloudinary_apy_secret,
        secure=True
    )

    @staticmethod
    def create_avatar_name(email: str, prefix: str):
        name = hashlib.sha256(email.encode()).hexdigest()[:12]
        return f"{prefix}/{name}"

    @staticmethod
    def upload(file, public_id):
        r = cloudinary.uploader.upload(file, public_id=public_id, overwrite=True)
        return r

    @staticmethod
    def get_avatar_url(public_id, version):
        src_url = cloudinary.CloudinaryImage(public_id).build_url(width=250, height=250, crop='fill', version=version)
        return src_url


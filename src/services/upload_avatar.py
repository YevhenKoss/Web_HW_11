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
        """
        The create_avatar_name function takes an email address and a prefix,
        and returns a string that is the name of the avatar image. The name is
        a hash of the email address with 12 characters from it.

        :param email: str: Specify the email address of the user
        :param prefix: str: Specify the prefix of the avatar name
        :return: A string
        """
        name = hashlib.sha256(email.encode()).hexdigest()[:12]
        return f"{prefix}/{name}"

    @staticmethod
    def upload(file, public_id):
        """
        The upload function takes a file and public_id as arguments.
        It then uploads the file to Cloudinary using the public_id provided.
        The function returns a dictionary containing information about the uploaded image.

        :param file: Specify the file to be uploaded
        :param public_id: Specify the name of the file that will be uploaded to cloudinary
        :return: A dictionary with the following keys
        """
        r = cloudinary.uploader.upload(file, public_id=public_id, overwrite=True)
        return r

    @staticmethod
    def get_avatar_url(public_id, version):
        """
        The get_avatar_url function takes in a public_id and version number,
            then returns the URL of the avatar image.

        :param public_id: Specify the image to be used
        :param version: Create a unique url for each image
        :return: A url for the avatar image
        """
        src_url = cloudinary.CloudinaryImage(public_id).build_url(width=250, height=250, crop='fill', version=version)
        return src_url


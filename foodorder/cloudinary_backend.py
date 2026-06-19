"""
Custom Cloudinary storage backend for Django 6.0+
Uses the cloudinary SDK directly without django-cloudinary-storage.
"""
import os
import cloudinary
import cloudinary.uploader
import cloudinary.api
from django.core.files.storage import Storage
from django.utils.deconstruct import deconstructible


cloudinary.config(
    cloud_name='dejers5zz',
    api_key='244943428161653',
    api_secret='15SbTvGfJ85gNiEGoolfYMs4GS4',
    secure=True,
)


@deconstructible
class CloudinaryStorage(Storage):
    """Django storage backend that saves files to Cloudinary."""

    def _save(self, name, content):
        # Strip the extension; Cloudinary handles format automatically
        public_id = os.path.splitext(name)[0].replace('\\', '/')
        response = cloudinary.uploader.upload(
            content,
            public_id=public_id,
            overwrite=True,
            resource_type='auto',
        )
        return response['public_id'] + '.' + response['format']

    def url(self, name):
        # Build the Cloudinary CDN URL
        public_id = os.path.splitext(name)[0]
        ext = os.path.splitext(name)[1].lstrip('.')
        return cloudinary.CloudinaryImage(public_id).build_url(format=ext, secure=True)

    def exists(self, name):
        try:
            public_id = os.path.splitext(name)[0]
            cloudinary.api.resource(public_id)
            return True
        except cloudinary.exceptions.NotFound:
            return False
        except Exception:
            return False

    def delete(self, name):
        try:
            public_id = os.path.splitext(name)[0]
            cloudinary.uploader.destroy(public_id)
        except Exception:
            pass

    def size(self, name):
        try:
            public_id = os.path.splitext(name)[0]
            resource = cloudinary.api.resource(public_id)
            return resource.get('bytes', 0)
        except Exception:
            return 0

    def get_available_name(self, name, max_length=None):
        return name

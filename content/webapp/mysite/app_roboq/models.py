from django.db import models
import os

# Create your models here.


class UploadIDS(models.Model):

    def get_upload_xml_path(instance, filename):
        return os.path.join(
            'xml',
            instance.char_username,
            filename)


    char_username =  models.CharField(
        max_length=255,
        unique=True,
        blank=False,
    )
    doc_xml = models.FileField(
        blank=False,
        upload_to=get_upload_xml_path
    )
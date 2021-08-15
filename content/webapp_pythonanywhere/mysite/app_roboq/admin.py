from django.contrib import admin
from .models import *
# Register your models here.


class UploadIDSAdmin(admin.ModelAdmin):
    pass

admin.site.register(UploadIDS, UploadIDSAdmin)

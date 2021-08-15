from django.urls import path
from .views import *


urlpatterns = [
    path('upload/', UploadExcel.as_view(), name='upload_excel'),
    path('download/', DownloadExcel.as_view(), name='download_xml')
]
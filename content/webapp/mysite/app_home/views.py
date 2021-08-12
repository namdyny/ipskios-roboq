from django.shortcuts import render
from django.views import View
from app_roboq.models import *

# Create your views here.


class HomeView(View):
    
    template_name = 'app_home/home.html'

    def get(self, request):
        # from django.conf import settings
        # import os
        # for root, dirs, files in os.walk(settings.STATIC_ROOT):
        #     print(root, dirs, files)

        try:
            upload_ids_instance = UploadIDS.objects.get(char_username=str(request.user))
        except:
            upload_ids_instance = 'none'

        print(upload_ids_instance)

        context = {
            'topnav_animate': 'svg-topnav-obj-roboq-rect',
            'upload_ids_instance': upload_ids_instance
        }

        return render(request, self.template_name, context)
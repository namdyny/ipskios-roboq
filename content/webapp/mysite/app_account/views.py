from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views import View
from django.contrib.auth.models import User
import json

# Create your views here.


class RegistrationView(View):
    
    template_name = 'app_account/registration.html'

    def get(self, request):

        context = {
            'topnav_animate': 'svg-topnav-obj-account-rect'
        }

        return render(request, self.template_name, context)

    def post(self, request):
        
        user = User.objects.create_user(request.POST['username'], request.POST['email'], request.POST['password'])

        return HttpResponseRedirect('/account/signin')

class RegistrationAJAXView(View):

    def get(self, request):

        data = {}
        is_exist = False
        username = request.GET['username']
        user = User.objects.filter(username=username)
        if len(user) > 0:
            is_exist = True
        data['is_exist'] = is_exist

        return HttpResponse(json.dumps(data), content_type="application/json")


class ProfileView(View):
    
    template_name = 'app_account/profile.html'
    
    def get(self, request):
        
        username = request.GET['username']

        context = {
            'topnav_animate': 'svg-topnav-obj-account-rect'
        }

        return render(request, self.template_name, context)
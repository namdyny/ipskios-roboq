from django.urls import path
from .views import *


urlpatterns = [
    path('registration', RegistrationView.as_view(), name='registration'),
    path('registration/ajax/', RegistrationAJAXView.as_view(), name='registrationAJAX'),
    path('profile/', ProfileView.as_view(), name='profile')
]
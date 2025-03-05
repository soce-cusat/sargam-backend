from django.urls import path, include
from .views import *

urlpatterns = [
	path('register/', RegistrationView.as_view(), name="register"),
	path('verify/<uidb64>/<token>/', verify_email, name='verify_email'),
    path('login/',user_login, name="user_login"),
    path('profile/',user_profile, name="user_profile"),


]
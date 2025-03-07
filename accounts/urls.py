from django.urls import path, include
from .views import *

urlpatterns = [
	path('register/', RegistrationView.as_view(), name="register"),
    path('reset/<str:uidb64>/<str:token>/', reset_password, name='reset_password'),
    path('login/',user_login, name="user_login"),
    path('forgot/',user_forgot_view, name="user_forgot"),
    path('logout/',user_logout, name="user_logout"),
    path('profile/',user_profile, name="user_profile"),
    path('remove/<int:pk>', remove_item_view, name="remove_item"),

]
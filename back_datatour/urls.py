from django.urls import path

from back_datatour.views import UserRegister

urlpatterns = [
    path("register/", UserRegister.as_view(), name='users_register')
]

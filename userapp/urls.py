from django.urls import path
from .views import *
# from .views import sign_in
# from . import views
# from userapp.views import


urlpatterns = [
    # /users/registration/
    path('registration/', registration, name='registration'),

    # /users/sign-in/
    path('sign-in/', sign_in, name='sign-in'),
    path('sign-out/', sign_out, name='sign-out'),
    
]
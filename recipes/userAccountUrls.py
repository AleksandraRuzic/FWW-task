from django.contrib import admin
from django.urls import path, include
from .userAccountViews import signUpView, logInView, logOutView, userView

urlpatterns = [
    path('', userView.as_view()),
    path('signup/', signUpView.as_view()),
    path('login/', logInView.as_view()),
    path('logout/', logOutView.as_view()),
]

"""
{
    "first_name":"Aleksandra",
    "last_name":"Ruzic",
    "username": "AleksUser",
    "email": "ruzic@ruzic.com",
    "password": "hopacupa25"
}
"""
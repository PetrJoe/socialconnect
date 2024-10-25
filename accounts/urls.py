from django.urls import include, path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('login/', login_view, name='login'), 
    path('register/',SignUpView.as_view(), name='register'),
    path('profile/<str:username>/', user_profile, name='user_profile'),
]
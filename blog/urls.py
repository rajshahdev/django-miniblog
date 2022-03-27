from unicodedata import name
from django.urls import path
from .views import home,about, dashboard, user_login, user_logout, user_signup
urlpatterns = [
    path('', home, name='home'),
    path('about/',about, name='about'),
    path('logout/',user_logout, name='logout'),
    path('login/',user_login, name='login'),
    path('dashboard/',dashboard, name='dashboard'),
    path('signup/',user_signup, name='signup'),
]
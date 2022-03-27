from unicodedata import name
from django.urls import path
from .views import home,about, dashboard, user_login, user_logout, user_signup, add_post, update_post, delete_post
urlpatterns = [
    path('', home, name='home'),
    path('about/',about, name='about'),
    path('logout/',user_logout, name='logout'),
    path('login/',user_login, name='login'),
    path('dashboard/',dashboard, name='dashboard'),
    path('signup/',user_signup, name='signup'),
    path('addpost/',add_post, name='addpost'),
    path('update/<int:id>/',update_post, name='update'),
    path('delete/<int:id>/',delete_post,name='delete')
]
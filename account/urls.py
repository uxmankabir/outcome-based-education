from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),

    path('login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),

    path('password_change/done/', views.password_change_done, name='password_change_done'),
    path('password_change/', views.password_change, name='password_change'),
    path('update_password/', views.update_password, name='update_password'),

]

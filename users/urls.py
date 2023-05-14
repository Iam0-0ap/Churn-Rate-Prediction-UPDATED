from django.urls import path
from . import views
from django.contrib.auth import views as auth_view

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('churn/', views.churn, name='churn'),
    path('login/', auth_view.LoginView.as_view(template_name='users/login.html'), name="login"),
    path('logout/', auth_view.LogoutView.as_view(template_name='users/logout.html'), name="logout"),
    path('result/',views.result,name="result"),
    path('discover/', views.discover, name="discover"),
    path('aboutus/', views.about, name="aboutus")
    
]

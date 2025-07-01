from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name="register"),
    path('user_login/', views.user_login, name="user_login"),
    path('logout/', views.logout, name="logout"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('', views.dashboard, name="dashboard"),
    
    path('activate/<uidb64>/<token>/', views.activate, name="activate"),
    
    path('forgotpassword/', views.forgotpassword, name="forgotpassword"),
    path('resetpassword_validate/<uidb64>/<token>/', views.resetpassword_validate, name="resetpassword_validate"),
    path('reset_password/', views.reset_password, name="reset_password"),
]

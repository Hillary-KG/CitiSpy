from django.urls import path
from . import views

#accounts urls

urlpatterns = [
    path('userLogin/', views.UserLogin.as_view(), name='login'),
    path('registerUser/', views.RegisterUserView.as_view(), name='register_user'),
    path('registerAdmin/', views.RegisterAdminView.as_view(), name='register_admin'),
    path('logout/', views.LogoutUser.as_view(), name='logout'),
]
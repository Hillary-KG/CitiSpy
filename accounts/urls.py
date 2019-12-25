from django.urls import path
from .views import UserLogin, RegisterDeptStaffView, RegisterUserView, RegisterAdminView

#accounts urls

urlpatterns = [
    path('userLogin/',UserLogin.as_view(), name='login'),
    path('registerDeptStaff/', RegisterDeptStaffView.as_view(), name='register_dept_staff'),
    path('registerUser/', RegisterUserView.as_view(), name='register_user'),
    path('registerAdmin/', RegisterAdminView.as_view(), name='register_admin'),
]
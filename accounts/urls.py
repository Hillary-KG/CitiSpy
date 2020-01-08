from django.urls import path
from django.contrib.auth import views as auth_views
from . import views, forms

#accounts urls

urlpatterns = [
    # path('userLogin/', auth_views.LoginView.as_view(template_name='accounts/login.html', authentication_form=forms.LoginForm ), name='login'),
    path('userLogin/', views.UserLogin.as_view(), name='login'),
    path('registerUser/', views.RegisterUserView.as_view(), name='register_user'),
    path('registerAdmin/', views.RegisterAdminView.as_view(), name='register_admin'),
    path('logout/', views.LogoutUser.as_view(), name='logout'),
    path('resetPassword/', auth_views.PasswordResetView.as_view(
        form_class = forms.CustPasswordResetForm,
        template_name = 'accounts/reset_password.html',
        email_template_name = 'accounts/reset_password_email.html',
        subject_template_name = 'accounts/subject_template.txt'
    ), name='reset_password'),
    path('resetPasswordDone/', auth_views.PasswordResetDoneView.as_view(
        template_name = 'accounts/reset_password_done.html'
    ), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name = 'accounts/reset_password_confirm.html',
        form_class = forms.PasswordResetForm,
        # success_url= '/reset/done/'
    ), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name = 'accounts/reset_password_complete.html'
    ), name='password_reset_complete'),
    # path('resetPassword/', views.ResetPassword.as_view(), name='reset_password'),
]
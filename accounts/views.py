from django.shortcuts import render, render_to_response
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from accounts.models import User
from accounts.forms import LoginForm, RegisterUserForm, RegisterAdmin, PasswordResetForm, CustomErrorList
from django.views.generic import View
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.auth.hashers import check_password
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordResetView

from .functions import password_generator

# from django.shortcuts import render


# Create your views here.
@csrf_protect
def login(request):
    form = LoginForm(request.POST or None, error_class=CustomErrorList)
    if request.is_ajax() and request.method == 'POST':
        print("entered form")
        if form.is_valid():
            print("form valid")
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(email=email)
                print("user obj", user)
                if user.check_password(form.cleaned_data['password']):
                    # 0-super admin, 1-dept admin,2-dept staff, 3-end user 
                    print("correct password")
                    if user.account_type == 4:
                        if user.last_login == None or user.last_login == '':
                            to = "verify"
                        else:
                            to = "user"
                    else:
                        if user.account_type == 2:
                            to = 'dept_admin'
                        elif user.account_type == 3:
                            to = 'dept_staff'
                        elif user.account_type == 1:
                            to = 'super_user'
                        else:
                            to = None
                    res = {'status':'ok', 'error':False, 'acc_type':to, 'data':user.email}
                else:
                    print("incorrect password")
                    res = {'status':'fail', 'error':'incorrect password'}
            except Exception as e:
                print("User not found!", e)
                res = {'status':'fail', 'error':'account not found'}
            return JsonResponse(res)  
    else: 
        form = LoginForm()
        
    return render(request, 'accounts/login.html', {'form': form})


@method_decorator(csrf_protect, name='post')
class UserLogin(View):
    """docstring for UserLogin"""
    template_name = 'accounts/login.html'
    form_class = LoginForm
    # authentication_form = LoginForm()
    
    def get(self, request):
        '''a func to work on the request.POST'''
        print("getting the form for you ")
        return render(request,self.template_name,{'form':self.form_class})

    def post(self, request):
        form = self.form_class(request.POST, error_class=CustomErrorList)
        print("go the data for you")
        if request.is_ajax():
            print("entered form")
            if form.is_valid():
                print("form valid")
                email = form.cleaned_data['email']
                try:
                    user = User.objects.get(email=email)
                    print("user obj", user)
                    if user.check_password(form.cleaned_data['password']):
                        # 0-super admin, 1-dept admin,2-dept staff, 3-end user 
                        print("correct password")
                        if user.account_type == 4:
                            if user.last_login == None or user.last_login == '':
                                to = "verify"
                            else:
                                to = "user"
                        else:
                            if user.account_type == 2:
                                to = 'dept_admin'
                            elif user.account_type == 3:
                                to = 'dept_staff'
                            elif user.account_type == 1:
                                to = 'super_user'
                            else:
                                to = None
                        res = {'status':'ok', 'error':False, 'acc_type':to, 'data':user.email}
                    else:
                        print("incorrect password")
                        res = {'status':'fail', 'error':'incorrect password'}
                except Exception as e:
                    print("User not found!", e)
                    res = {'status':'fail', 'error':'account not found'}
                return JsonResponse(res)
            else:
                # print("form invalid")
                print("form errors", form.errors)
                res = {'status':'fail', 'form_errors':form.errors, }
                return JsonResponse(res)
                # return super().form_valid(form)

class LogoutUser(LogoutView):
    template_name = 'accounts/logout.html'
    def get(self, request):
        return render(request, self.template_name,{})




@method_decorator(csrf_protect, name='dispatch')
@method_decorator(login_required,name='post')
class ResetPassword(PasswordResetView):
    template_name = 'accounts/reset_password.html'
    # form_class = 



@method_decorator(csrf_protect, name='dispatch')
@method_decorator(csrf_protect, name='post')
@method_decorator(login_required, name='post')
class RegisterUserView(View):
    template_name = 'accounts/register_admin.html'
    def get(self, request):
        form = RegisterUserForm()
        return render(request, self.template_name, {'form':form})

    def post(self, request):
        form = RegisterUserForm(request.POST or None)
        user_type = request.user.account_type
        if form.is_valid():
            try:
                form.save()
                print("data saving ....")
                email = form.cleaned_data['email_address']
                res = {'status':'success', 'email':email, 'user':user_type}
            except Exception as e:
                print("an error occured while saving user", e)
                res = {'status':'fail', 'error':'user saving error', 'user':user_type}
                return JsonResponse(res)
        else:
            res =  {'status':'fail', 'user':user_type, 'error': form.errors}
            return JsonResponse(res)


@method_decorator(csrf_protect, name='post')
class RegisterAdminView(View):
    """docstring for RegisterAdminView"""
    template_name = 'accounts/register_admin.html'

    def get(self, request):
        form = RegisterAdmin()

        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = RegisterAdmin(self.request.POST)
        print(self.request.POST)
        if request.is_ajax():
            if form.is_valid():
                print("form data:",form.cleaned_data)
                try:
                    form.save()
                    print("saved data successfully")
                except Exception as e:
                    print(e)
                    res = {'status': "fail", 'error':"db error"}
                else:
                    res = {'status': "success", 'error': False}
            else:
                # print("form data:",form.cleaned_data)
                print("form errors", form.errors)
                res = {'status': "invalid", 'error': form.errors}
        return JsonResponse(res)
        
            



   
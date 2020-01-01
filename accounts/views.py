from django.shortcuts import render, render_to_response
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from accounts.models import User
from accounts.forms import LoginForm, RegisterUserForm, RegisterAdmin, ChangePasswordForm
from django.views.generic import View
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.auth.hashers import check_password
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
# from django.shortcuts import render



from .functions import password_generator
# Create your views here.

@method_decorator(csrf_protect, name='post')
class UserLogin(LoginView):
    """docstring for UserLogin"""
    template_name = 'accounts/login.html'
    
    def get(self, request):
        '''a func to work on the request.POST'''
        form = LoginForm()
        return render(request,self.template_name,{'form':form})

    def post(self, request):
        form = LoginForm(request.POST)
        if request.is_ajax():
            if form.is_valid():
                email = form.cleaned_data['email']
                password = form.cleaned_data['password']
                try:
                    user = User.objects.get(email=email)
                    if user.check_password(password):
                        # 0-super admin, 1-dept admin,2-dept staff, 3-end user 
                        if user.account_type == 4:
                            if user.last_login == None or user.last_login == '':
                                to = "verify"
                        else:
                            if user.account_type == 2:
                                to = 'dept_admin'
                            elif user.account_type == 3:
                                to = 'dept_staff'
                            elif user.account_type == 1:
                                to = 'super_user'
                            else:
                                to = None
                        res = {'status':'ok', 'error':False, 'acc_to':to, 'data':user.email}
                    else:
                        res = {'status':'fail', 'error':'incorrect password'}
                except Exception as e:
                    print("User not found!", e)
                    res = {'status':'fail', 'error':'account not found'}
            else:
                res = {'status':'fail', 'error':form.errors}
        return JsonResponse(res)

class LogoutUser(LogoutView):
    template_name = 'accounts/logout.html'
    def get(self, request):
        return render(request, self.template_name,{})



@login_required
@method_decorator(csrf_protect, name='post')
class ChangePassword(PasswordChangeView):
    template_name = 'accounts/reset_password.html'
    form_class = ChangePasswordForm()


# @method_decorator(csrf_protect, name='dispatch')
# @method_decorator(csrf_protect, name='post')
# class RegisterDeptStaffView(View):
#     template_name = 'accounts/register_dept_staff.html'
#     def get(self, request):
#         form = RegisterAdmin()
#         return render(request, self.template_name, {'form':form})

#     def post(self, request):
#         print(self.request.POST)

#         first_name = self.request.POST['first_name']
#         last_name = self.request.POST['last_name'],
#         email = self.request.POST['email']
#         phone_number = self.request.POST['phone_number']
#         account_type = self.request.POST['account_type']
#         staff_number = self.request.POST['staff_number']
#         u_name = (self.request.POST['first_name']+'_'+self.request.POST['last_name'])
#         password = PasswordGenerator().generate()
#         # print("password generated", password)
#         form = RegisterAdmin(self.request.POST)
        
#         if form.is_valid():
#             try:
#                 # form.save()
#                 User.objects.create(username=email, first_name=first_name, last_name=last_name, email=email, account_type=account_type
#                     , phone_number=phone_number, password=password)
#                 print("data saving ....")
#                 email = form.cleaned_data['email']
#                 res = {'status':'success', 'email':email, 'user': int(self.request.POST['account_type'])}
#             except Exception as e:
#                 print("an error occured while saving user", e)
#                 res = {'status':'fail', 'error':'user saving error', 'user': self.request.POST['account_type']}
#             return JsonResponse(res)
            
#         else:
#             # print("form invalid", form.errors)
#             res =  {'status':'fail', 'user':user_type, 'error': form.errors}
#             return JsonResponse(res)


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
                # username = form.cleaned_data['username']
                # email = form.cleaned_data['email']
                # phone_number = form.cleaned_data['phone_number']
                # password = form.cleaned_data['password']
                # confirm_password = form.cleaned_data['confirm_password']
                try:
                    # user = User.objects.create(username=username, email=email, phone_number=phone_number, is_superuser=True,
                    #         account_type=0, is_staff=True)
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
        
            



   
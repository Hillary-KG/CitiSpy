from django.shortcuts import render
from django.views.generic import View
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.contrib.sessions.backends.db import SessionStore

from accounts.forms import RegisterAdmin


# Create your views here.
@method_decorator(login_required, name='post')
@method_decorator(csrf_protect, name='post')
@method_decorator(login_required, name='get')
class DashboardView(View):
    """blueprint for the emergency dept dashboard: dept staff/admin registration(admins only)
    alert statistics - analysis and prediction, receiving alerts in real-time
    """
    template_name = 'em_dept/dashboard.html'

    # @csrf_protect
    def get( self, request):
        admin_form = RegisterAdmin()
        context = {
                'admin_form': admin_form,
            }

        if request.user.is_authenticated:
            print("yes")
        else:
            print("No user")

        return render(request, self.template_name, context)


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
    
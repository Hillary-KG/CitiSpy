from django.shortcuts import render
from django.views.generic import View
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.contrib.sessions.backends.db import SessionStore


# Create your views here.
class DashboardView(View):
    """blueprint for the emergency dept dashboard: dept staff/admin registration(admins only)
    alert statistics - analysis and prediction, receiving alerts in real-time
    """
    template_name = 'em_dept/dashboard.html'

    def get( self, request):
        return render(request, self.template_name, {})


    def post():
        pass

        
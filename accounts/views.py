from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.


def dashboard_redirect(request):
    return HttpResponse("Redirecting user based on role...")

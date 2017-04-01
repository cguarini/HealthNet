from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, render_to_response, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import  login_required,PermissionDenied
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.models import Group

# Create your views here.

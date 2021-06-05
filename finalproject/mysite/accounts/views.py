from django.shortcuts import render, redirect
# accounts/views.py
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

# View for signing up new users
class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy(' ')
    template_name = 'polls/signup.html' # connect to template
    def post(self, request):
        newUser = User(
                    username = request.POST['username'],
                    password = make_password(request.POST['password1'])
        )
        newUser.save() # get User information saved to database

        # set up user system for passwords
        user = authenticate(username=request.POST['username'],
            password=request.POST['password1'])
        if user is not None:
            login(request,user)
        else:
            pass

        return redirect('../../polls/')


# Create your views here.

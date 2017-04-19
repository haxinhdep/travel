from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth

from django.contrib.auth import logout
from django.db import IntegrityError


def not_authorized(request):
    return HttpResponse("No authorized. 403")


def home(request):
    return render(request, "main_home/home.html", "")


def index(request):
    return render(request, 'index.html')

    # next = request.GET.get('next', '/home/')
    # if request.method == "POST" :
    #     username = request.POST['username']
    #     password = request.POST['password']
    #     user = authenticate(username=username, password=password)
    #
    #     if user is not None:
    #         if user.is_active:
    #             login(request, user)
    #             return HttpResponseRedirect(next)
    #         else:
    #             return HttpResponse("Inactive user.")
    #     else:
    #         render(request, "404/404-error.html", "")
    #
    # return render(request, "main_home/index.html", {'redirect_to': next})
    # # return render(request, "main_home/index.html", "")


def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/')


# def singup(request):
#     username = request.POST['signup_username']
#     email = request.POST['signup_email']
#     password = request.POST['signup_password']
#     first_name = request.POST['signup_first_name']
#     last_name = request.POST['signup_last_name']
#     confirmPassword = request.POST['signup_confirmPassword']
#
#     try:
#         if password == confirmPassword:
#             user = User.objects.create_user(
#                 username=username, email=email, password=password)
#             if 'partner':
#                 user.is_staff = 1
#             user.first_name = first_name
#             user.last_name = last_name
#             user.save()
#             return HttpResponseRedirect("/index/", {'success': 'Successfully LoggedIn.'})
#         else:
#             raise forms.ValidationError("You forgot to retype your password.")
#     except IntegrityError:
#         return render(request, '404/404-erorr.html', {'error': 'User already exists!! Try forgot password.'})
#
#
# def singin(request):
#     if request.user.is_authenticated():
#         return HttpResponseRedirect("/home/", {'success': 'Successfully LoggedIn.'})
#
#     if 'signIn_email' in request.POST:
#         user_name = request.POST['signIn_email']
#         password = request.POST['signIn_password']
#         user = auth.authenticate(username=user_name, password=password)
#         if user is not None and user.is_active:
#             # Correct password, and the user is marked "active"
#             auth.login(request, user)
#             # Redirect to a success page.
#             return HttpResponseRedirect("/index/", {'success': 'Successfully LoggedIn.'})
#         else:
#             # Show an error page
#             return render(request, '404/404-error.html', {'error': 'Invalid user try signup!!'})
#     else:
#         return render(request, 'main_home/index.html')
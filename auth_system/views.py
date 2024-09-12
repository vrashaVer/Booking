from django.shortcuts import render, redirect
from django.contrib.auth import login 
from django.contrib.auth.forms import AuthenticationForm
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from .forms import UserRegistrationForm
from django.contrib.auth.models import User


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            current_site = get_current_site(request)
            mail_subject = 'Activate your account.'
            message = render_to_string('auth_system/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            send_mail(mail_subject, message, 'from@example.com', [user.email])

            return redirect('account_activation_sent')
    else:
        form = UserRegistrationForm()
    return render(request, template_name='auth_system/register.html', context={'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('rooms_list')
    else:
        form = AuthenticationForm()
    return render(request, template_name='auth_system/login.html', context={'form': form})

def activate(request, uidb64, token):
    try:
        uid =  force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('rooms_list')
    else:
        return render(request, 'auth_system/account_activation_invalid.html')


def account_activation_sent(request):
    return render(request, 'auth_system/account_activation_sent.html')

def account_activation_invalid(request):
    return render(request, 'auth_system/account_activation_invalid.html')
























# from django.shortcuts import render,redirect
# from django.contrib.auth.forms import AuthenticationForm
# from auth_system.forms import CustomUserCreateForm
# from django.contrib.auth import login,authenticate
# from django.contrib import messages

# def register(request):
#     if request.method == "POST":
#         form = CustomUserCreateForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             login(request,user)
#             return redirect("rooms_list")
#     else:
#         form = CustomUserCreateForm()

#     return render(request, template_name="auth_system/register.html", context={"form":form})

# def login(request):
#     if request.method == "POST":
#         form = AuthenticationForm(request, data=request.POST)
#         if form.is_valid():
#             username = form.cleaned_data.get("username")
#             password = form.cleaned_data.get("password")
#             user = authenticate(request, username=username,password=password)
#             if user is not None:
#                 login(request,user)
#                 return redirect("rooms_list")
#             else:
#                 messages.error(request,message='Wrong username and password')
#     else:
#         form = AuthenticationForm()
#     return render(request, template_name="auth_system/login.html", context={"form":form})
        





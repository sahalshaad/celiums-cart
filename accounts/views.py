from django.contrib import messages, auth
from django.http import HttpResponse
from django.shortcuts import redirect, render

from carts.models import Cart, CartItem
from carts.views import _cart_id
from .forms import RegistrationForm
from .models import Account
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            password = form.cleaned_data['password']
            
            username = email.split("@")[0]
            
            user = Account.objects.create_user (first_name=first_name, last_name=last_name, email=email, username=username, password=password)
            user.phone = phone
            user.save()
            
            # USER ACTIVATION
            current_site = get_current_site(request)
            mail_subject = 'Please activate your account'
            message = render_to_string('accounts/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
            
            # messages.success(request, "Thank you for registration with us!. we have send an verification code in your email.. please verify!")
            return redirect ('/accounts/user_login/?command=verification&email='+email)
    else:
        form = RegistrationForm()
    context = {
        'form':form
    }
    return render (request, 'accounts/register.html', context)



def user_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        
        user = auth.authenticate(email=email, password=password)
        if user is not None:
            try:
                cart = Cart.objects.get(cart_id = _cart_id(request))
                is_cart_item_exists = CartItem.objects.filter(cart=cart).exists()
                if is_cart_item_exists:
                    cart_item = CartItem.objects.filter(cart=cart)
                    
                    for item in cart_item:
                        item.user = user
                        item.save()
            except:
                pass
            auth.login(request, user)
            # messages.success(request, 'You are logged in')
            return redirect ('home')
        else:
            messages.error(request, 'Something error please try again')
            return redirect ('user_login')
    return render (request, 'accounts/login.html')



@login_required(login_url='user_login')
def logout(request):
    auth.logout(request)
    messages.success(request, 'You are logged out')
    return redirect('user_login')


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None
        
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Congratulations your account is activated')
        return redirect ('user_login')
    else:
        messages.error(request, 'Invalid activation link')
        return redirect ('register')
    
    
@login_required(login_url='user_login')
def dashboard(request):
    return render (request, 'accounts/dashboard.html')



def forgotpassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)
            
            # RESET PASSWORD 
            current_site = get_current_site(request)
            mail_subject = 'reset your password'
            message = render_to_string('accounts/reset_password_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
            
            messages.success(request, 'Password reset has been sent to your registerd email address')
            return redirect ('user_login')
            
        else:
            messages.error(request, 'Account dose not Exists!!!')
            return redirect ('forgotpassword')
            
    return render (request, 'accounts/forgotpassword.html')

def resetpassword_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None
        
    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'Please reset your password')
        return redirect ('reset_password')
    else:
        messages.error(request, 'This link has been expired')
        return redirect ('user_login')
    
def reset_password(request):
    if request.method == 'POST':
        password = request.POST["password"]
        confirm_password = request.POST["confirm_password"]
        
        if password == confirm_password:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'password reset successfull')
            return redirect ('user_login')
        else:
            messages.error(request, 'password is not match')
            return redirect ('reset_password')
    else:
        return render (request, 'accounts/reset_password.html')
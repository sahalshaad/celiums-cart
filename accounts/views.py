from django.contrib import messages, auth
from django.shortcuts import redirect, render
from .forms import RegistrationForm
from .models import Account
from django.contrib.auth.decorators import login_required

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
            mail_subject = 'Please Activate Your Account'
            message = render_to_string('accounts/account_activation_email.html')
            
            messages.success(request, "registration is success")
            return redirect ('register')
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
from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required
from .forms import createUserForm,UserUpdateForm,ProfileUpdateForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.utils.encoding import force_bytes,force_str
from django.core.mail import EmailMessage


from .token import account_activate_token

def activate( request,uidb64, token):
    # User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)

    except:
        user =None
    if user is not None and account_activate_token.check_token(user, token ):
        user.is_active =True
        user.save()
        messages.success(request, f'Thank you for your email confirmation . now you login your account')
        redirect("login")
    else:
        messages.error(request, f'Activation link is invalid!')
        
    return redirect("blog-home")

def activateEmail(request, user,to_email):
    mail_subject = "Activate your account ."
    message = render_to_string("users/activate_account.html",{
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid':urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activate_token.make_token(user),
        "protocol": 'https' if  request.is_secure() else 'http'
    })
    email = EmailMessage( mail_subject, message , to=[to_email])
    if email.send():
        messages.success(request, f'Dear <b>{user.username}</b>,please go to your email <b>{to_email}</b> inbox and click on\
                        received activation link to confirm and complete the registration. <b>Note:</b> Check your spam folder.')
    else:
        messages.error(request, f'Problem sending email to {to_email} check if you type it correctly ')

def register(request):
    form = createUserForm()
    if request.method== 'POST':
        
         form = createUserForm(request.POST)
         if form.is_valid():
            user = form.save(commit=False)
            user.is_active=False
            user.save()
            activateEmail(request,user,form.cleaned_data.get('email'))
            # messages.success(request, f'Your account has been created! {user.username}')
            return redirect('login')
         else:
             for error in list(form.errors.values()):
                messages.error(request,error)

    else:
        form = createUserForm()
        
    context={'form': form}
        # username=request.POST.get('username')
        # email=request.POST.get('email')
        # pass1=request.POST.get('pass1')
        # pass2=request.POST.get('pass2')
    
        # if pass1 != pass2 :
        #      messages.info(request, f'your first and second password are different')
        # else :
        #     my_user = User.objects.create_user(username,email,pass1)
        #     my_user.save()
        #     messages.success(request, f'Your account has been created! You are now able to log in')
        #     return redirect('login')
    
    return render(request, 'users/register.html',context)


def login_1(request):
    if request.method== 'POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        # print(username,password)
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            messages.success(request, f' User connect succesfully !!')
            return redirect('blog-home')
        else:
            messages.error(request, f'it can be in your username or the password that sended the error')
        
    return render(request, 'users/login.html')

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'users/profile.html', context)


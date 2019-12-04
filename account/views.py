from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import RegistrationForm, AccountAuthenticationForm, AccountUpdateForm


def registration_view(request):
    context = {}

    # if the form is post request then if there is no issue then save it and ...
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()

            # get the data from a valid form  =>
                                # we refrence the form the cleaned_data =>
                                                            # then get the parameter
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')

            # create the account
            account = authenticate(email = email, password = raw_password)

            # now that we have that user object
                     # then we can call login
            login(request, account)

            # after login rediret to home
                # where is home ? => in home directory(auto_what) urls we have named home the path
                                                                            # [path('', home_screen, name="home"),]
            return redirect('home')

        # if the form is not valid
        else:
            context['registration_form'] = form

    # if the request is not a post request so its get request so
                            # that means they are visiting registration form for the first time
    else:
        form = RegistrationForm()
        context['registration_form'] = form

    return render(request, 'account/register.html', context)


def logout_view(request):
    logout(request)
    return redirect("home")

def login_view(request):
    context = {}    #just like other views

    user = request.user
    if user.is_authenticated:       # if user is authenticated they don't neet to be on the login page
        return redirect("home")

    # if they are not authenticated then we shall proceed
    if request.POST:    # a post request is made on login form
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)

            if user: # if every thing above is correct then user exists and
                login(request, user)
                return redirect("home")

    # if it is not a post request that means that they are in login page but they are not attempting to login
    else:
        form = AccountAuthenticationForm()

    context['login_form'] = form
    return render(request, 'account/login.html', context)

def accoutn_view(request):

    if not request.user.is_authenticated:
        return redirect("login")
    context = {}

    if request.POST:
        form = AccountUpdateForm(request.POST, instance=request.user) # user because in pk form we are getting pk of user
        if form.is_valid():
            form.initial = {
                "email" : request.POST['email'],
                "username": request.POST['username'],
            }
            form.save()
            context['success_message'] = "تغییرات با موفقیت ذخیره شد."
    else:
        form = AccountUpdateForm(
            # values that are gonna be desplay as soon as the visit their profile
            initial={
                "email": request.user.email,
                "username": request.user.username,
            }
        )

    context['account_form'] = form


    return render(request, "account/account.html", context)


def must_authenticate_view(request):
	return render(request, 'account/must_authenticate.html', {})



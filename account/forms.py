from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate #this authenticate checks user if their cridential is valid or not
from .models import Account


class RegistrationForm(UserCreationForm):
    email               = forms.EmailField(max_length=60, help_text='Required. Add a valid email address')


    class Meta:
        model = Account

        # telling the registration form that what form might looks like
        fields = ("email", "username", "password1", "password2")


class AccountAuthenticationForm(forms.ModelForm):
    password                = forms.CharField(label='Password', widget=forms.PasswordInput) #star typing passwords

    class Meta:
        model = Account                 # what kind of fields is it expecting to see
        fields = ('email', 'password')  # which fields are gonna be visible

    def clean(self):                    # this function is available to any form that extends the model form
            # this method is like a interceptor that means :
                    # that before the form can do anything it has to run this clean method and any logic that we write
                    # in this clean method
            # with this we are going to authenticate user if it's valid or not
        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']
            if not authenticate(email=email, password=password):
                raise forms.ValidationError("نام کاربری یا پسور اشتباه می باشد.")



class AccountUpdateForm(forms.ModelForm):

    class Meta:
        model = Account
        fields = ('email', 'username')

    # clean individual property rather than going through all properties and it will run whether it is valid or not
    def clean_email(self):
        if self.is_valid(): # we need to make sure that field is valid and it does not equal other email that is already in database
            email = self.cleaned_data['email']
            try:
                # if account exist
                account = Account.objects.exclude(pk=self.instance.pk).get(email=email)
            except Account.DoesNotExist:
                return email
            raise forms.ValidationError('Email "%s" is already in use.' % email)    # clean individual property rather than going through all properties and it will run whether it is valid or not

    def clean_username(self):
        if self.is_valid(): # we need to make sure that field is valid and it does not equal other email that is already in database
            username = self.cleaned_data['username']
            try:
                # if account exist
                account = Account.objects.exclude(pk=self.instance.pk).get(username=username)
            except Account.DoesNotExist:
                return username
            raise forms.ValidationError('Username "%s" is already in use.' % username)



from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


# create custom user manager
class MyAccountManager(BaseUserManager):
    # we are passing email and username because these two are required fiels (email to login and username is required)
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError("ایمیل خود را وارد کنید")
        if not username:
            raise ValueError("نام کاربری را وارد کنید")

        # if two if is done then what -> create user
        user = self.model(
            email = self.normalize_email(email),
            username = username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user


    # create superuser
    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username,
        )
        user.is_admin       = True
        user.is_staff       = True
        user.is_superuser   = True
        user.save(using=self._db)
        return user



class Account(AbstractBaseUser):
    #custom
    email                   = models.EmailField(verbose_name="ایمیل", max_length=60, unique=True)
    username                = models.CharField(verbose_name="نام کاربری", max_length=30, unique=True)
    #phonenumber             = models.IntegerField(verbose_name="شماره تماس", unique=True)


    # these are required to create a custom user
    date_joined             = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    last_login              = models.DateTimeField(verbose_name="last login", auto_now=True)
    is_admin                = models.BooleanField(default=False)
    is_active               = models.BooleanField(default=True)
    is_staff                = models.BooleanField(default=False)
    is_superuser            = models.BooleanField(default=False)


    # with what users shall login
    USERNAME_FIELD = 'email'

    # set what is required while registering
    REQUIRED_FIELDS = ['username',]

    # where the manager is and how to use it
    objects = MyAccountManager()

    # what they see when they login to their page
    def __str__(self):
        return self.email

    # these functions are required to make a custom user model ( they are actually permissions)
    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True














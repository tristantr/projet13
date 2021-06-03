from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


class UserManager(BaseUserManager):
    """Manager for the User Model"""

    def create_user(
        self,
        email,
        pseudo=None,
        password=None,
        is_active=True,
        is_staff=False,
        is_admin=False
    ):
        """Creates and saves a User with the given email and password"""
        if not email:
            raise ValueError("Users must have an email address")
        if not pseudo:
            raise ValueError("Users mus have a pseudo")             
        if not password:
            raise ValueError("Users must have a password")

        user = self.model(email=self.normalize_email(email))
        user.pseudo = pseudo
        user.set_password(password)

        user.staff = is_staff
        user.admin = is_admin
        user.active = is_active
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, password=None):
        """Creates and saves a superuser with the given email and password"""
        user = self.create_user(email, pseudo=pseudo, password=password, is_staff=True)
        return user

    def create_superuser(self, email, pseudo, password=None):
        """Creates and saves a superuser with the given email and password"""
        user = self.create_user(
            email=email,
            pseudo=pseudo,
            password=password,
            is_staff=True,
            is_admin=True
            )
        return user


class User(AbstractBaseUser):
    """User model"""

    username = None
    email = models.EmailField(
        verbose_name="email address",
        max_length=255, unique=True)
    pseudo = models.CharField(max_length=20, default='pseudo')    
    is_active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)  # a admin user, non super-user
    admin = models.BooleanField(default=False)  # a superuser

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["pseudo"]  # USERNAME_FIELD & Password are required by default

    objects = UserManager()

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer= Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.staff

    @property
    def is_admin(self):
        "Is the user a admin member?"
        return self.admin

class Favorite(models.Model):
    """ Favorite model """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    place = models.CharField(max_length=100, default="key")

class CommentManager(models.Manager): 
    """" Manager for the Comment Model """ 

    def add_commment(self, place, user, body):
        place = self.create(
            place=place,
            user=user,
            body=body,
            )
        return place

class Comment(models.Model):
    place = models.CharField(max_length=100, default="key")
    user = models.ForeignKey(User, related_name="comments", on_delete=models.CASCADE)
    body = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    objects = CommentManager()

    def __str__(self):
        return '%s - %s %s' % (self.user, self.body, self.date_added)

    def get_comment(self):
        comment = {
        'place': self.place,
        'user': self.user.pseudo,
        'body': self.body,
        'date_added': self.date_added
        }
        return comment




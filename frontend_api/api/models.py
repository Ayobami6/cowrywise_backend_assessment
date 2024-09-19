from django.db import models
from django.contrib.auth.models import AbstractBaseUser, UserManager
from django.contrib.auth.models import PermissionsMixin
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.utils.translation import gettext_lazy as _
from typing import Any
from django.db import transaction
from django.utils import timezone
from sparky_utils.decorators import str_meta
from django.utils import timezone
# Create your models here.


class CustomUserManager(UserManager):

    # validate email
    @staticmethod
    def validate_email(email: str) -> None:
        """
        This method validates the email address of a user.
        """
        try:
            validate_email(email)
        except ValidationError:
            raise ValidationError(
                message=_("Please enter a valid email address."))

    # create user method
    def create_user(
        self, email: str, password: str = "", **extra_fields: Any
    ) -> Any:
        """
        This method creates a user with the specified email address, username, and password.
        """
        if not email:
            raise ValidationError(message="Users must have an email address.")
        with transaction.atomic():
            user = self.model(email=email, **extra_fields)
            user.set_password(password)
            user.save(using=self._db)
            return user
    def create_superuser(self, email: str, password: str, **extra_fields: Any) -> Any:
        """
        This method creates a superuser with the specified email address, username, and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        
        if not password:
            raise ValueError("Password must be provided")
          
        user = self.create_user(email, password, **extra_fields)
        
        user.save(using=self._db)
        return user
        
        
class User(AbstractBaseUser, PermissionsMixin):
    objects = CustomUserManager()
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    is_staff = models.BooleanField(
        _('admin status'),
        default=False,
        help_text=_(
            'Designates whether the user can log into this admin site.'),
    )
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    class Mete:
        db_table: str = "users"
        verbose_name: str = "User"
        verbose_name_plural: str = "Users"

    def __str__(self) -> str:
        return self.email

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"


@str_meta
class Category(models.Model):
    name = models.CharField(max_length=30)

@str_meta
class Book(models.Model):
    title = models.CharField(max_length=50, help_text=_("Book Title"))
    author = models.CharField(max_length=30, help_text=_("Author"))
    publisher = models.CharField(max_length=30, help_text=_("Publisher"))
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    available = models.BooleanField(default=True)
    available_date = models.DateField(null=True, blank=True)
    
@str_meta    
class BorrowedBookLog(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="borrowed_books")
    borrow_date = models.DateField(default=timezone.now)
    return_date = models.DateField()
    
    
    
def save_user(data):
    user = User.objects.create_user(email=data["email"], password=data["password"], first_name=data["first_name"], last_name=data["last_name"])
    return user
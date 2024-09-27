from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _
# Create your models here.


# class User(AbstractUser):
#     username = models.CharField(max_length=100)
#     email = models.EmailField(unique=True)

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['username']


#     def profile(self):
#         profile, created = Profile.objects.get_or_create(user=self)
#         return profile

# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE) # 
#     full_name = models.CharField(max_length=1000)
#     bio = models.CharField(max_length=100)
#     image = models.ImageField(upload_to="user_images", default="default.jpg")
#     verified = models.BooleanField(default=False)

#     def save(self, *args, **kwargs):
#         if self.full_name == "" or self.full_name == None:
#             self.full_name = self.user.username
#         super(Profile, self).save(*args, **kwargs)

# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)

# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()

# post_save.connect(create_user_profile, sender=User)# User
# post_save.connect(save_user_profile, sender=User)

# # Todo List
# class Todo(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     title = models.CharField(max_length=1000)
#     completed = models.BooleanField(default=False)
#     date = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.title[:30]

# # Chat App Model
# class ChatMessage(models.Model):
#     user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="user")
#     sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="sender")
#     reciever = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="reciever")

#     message = models.CharField(max_length=10000000000)

#     is_read = models.BooleanField(default=False)
#     date = models.DateTimeField(auto_now_add=True)
    
#     class Meta:
#         ordering = ['date']
#         verbose_name_plural = "Message"

#     def __str__(self):
#         return f"{self.sender} - {self.reciever}"

#     @property
#     def sender_profile(self):
#         sender_profile = Profile.objects.get(user=self.sender)
#         return sender_profile
#     @property
#     def reciever_profile(self):
#         reciever_profile = Profile.objects.get(user=self.reciever)
#         return reciever_profile
    

class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    bio = models.CharField(max_length=255, blank=True)
    full_name = models.CharField(max_length=255, blank=True)
    # EMAIL_FIELD = 'email'

    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.username

class CustomGuest(models.Model):
    fullname = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    telephone = models.CharField(unique=True, max_length=100)

    def __str__(self) -> str:
        return self.telephone
 
class Room(models.Model):
    room_name = models.CharField(max_length=255, unique=True)
    # user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True, related_name='rooms')
    user = models.ForeignKey(CustomGuest, on_delete=models.CASCADE, null=True, blank=True, related_name='rooms')
    def __str__(self):
        return self.room_name
    
    def return_room_messages(self):
        return ChatMessage.objects.filter(room=self)
    
    def create_new_room_message(self, sender, message):

        new_message = ChatMessage(room=self, sender=sender, message=message)
        new_message.save()

class ChatMessage(models.Model):
    message = models.CharField(max_length=1000)
    date = models.DateTimeField(auto_now_add=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    sender = models.CharField(max_length=255)

    def __str__(self) -> str:
        return f"{self.message} - {self.date}"
    
   




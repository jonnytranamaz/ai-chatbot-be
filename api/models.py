from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _

class Symptom(models.Model):
    name = models.CharField(max_length=10000)

    def __str__(self) -> str:
        return self.name
    
class ChatTurn(models.Model):
    user_request = models.CharField(max_length=10000)
    bot_response = models.CharField(max_length=10000)

class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    use_in_migrations = True

    def create_user(self, telephone, password=None, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not telephone:
            raise ValueError(_('The Telephone must be set'))
        
        user = self.model(telephone=telephone, username=telephone, **extra_fields)

        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, telephone, password, **extra_fields):
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
        return self.create_user(telephone, password, **extra_fields)
    

    


class CustomUser(AbstractUser):
    fullname = models.CharField(max_length=100, blank=True)
    age = models.PositiveIntegerField(blank=True, default=1)
    telephone = models.CharField(_('telephone'), unique=True, max_length=12) #, primary_key=True

    USERNAME_FIELD = 'telephone'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self) -> str:
        return self.telephone

    

# Cac models chinh thuc
class Conversation(models.Model):
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conversation {self.id} by {self.sender.telephone}"
    
class Message(models.Model):
    OWNER_TYPE_CHOICES = [
        ('enduser', 'End User'),
        ('bot', 'Bot'),
    ]
    MESSAGE_TYPE_CHOICES = [
        ('text', 'Text'),
        ('image', 'Image'),
        ('file', 'File'),
    ]
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    owner_type = models.CharField(max_length=255, choices=OWNER_TYPE_CHOICES, default='bot')
    timestamp = models.DateTimeField(auto_now_add=True)
    content = models.TextField(blank=True)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    file = models.FileField(upload_to='files/', null=True, blank=True)
    message_type = models.CharField(max_length=255, choices=MESSAGE_TYPE_CHOICES, default='text')

    def __str__(self):
        return f"Message {self.id} in Conversation {self.conversation.id} by {self.sender.telephone if self.sender else 'Bot'}"

class TrainingMessage(models.Model):
    request = models.TextField()
    response = models.TextField()

    def __str__(self):
        return f"Request: {self.request[:50]}... Response: {self.response[:50]}..."

from django.contrib.auth.models import AbstractUser
from django.db import models
from .user_managers import CustomUserManager

class User(AbstractUser):
    """ Custom User Model to make email as username/login field """
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

class FriendRequest(models.Model):
    """ 
        FriendRequest Model to save friend requests instances with fields:
            sender:= User who sent the friend request.
            receiver:= User who received the friend request.
            timestamp:= Date and time when the friend request is sent/received
            status:= It's a choice/dropdown field, to check if the friend_request is pending, accepted or rejected.       
    """
    
    sender = models.ForeignKey(User, related_name='sent_requests', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_requests', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')], default='pending')
    
    class Meta:
        unique_together = ('sender', 'receiver') # Sender<->receiver should be unique

    def __str__(self):
        return f"{self.sender} to {self.receiver} - {self.status}"
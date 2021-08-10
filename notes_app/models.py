from django.db import models
from django.contrib.auth.models import User
import datetime

# babor, babor; emon, 12345emon
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='user_images', blank=True, null=True)
    is_subscribed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('user',)
    def __str__(self):
        return self.user.username

class SubscriptionType(models.Model):
    title = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created_at',)
    def __str__(self):
        return self.title
    

class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created_at',)
    def __str__(self):
        return self.user.username +'-'+self.title


subs = SubscriptionType.objects.all()
SUBSCRIPTION_CHOICES = ([(str(subs), str(subs)) for subs in subs])

class Subscription(models.Model):
    title = models.CharField(max_length=200)
    subscription_type = models.CharField(choices=SUBSCRIPTION_CHOICES, max_length=200, default=None)
    day_limit = models.PositiveIntegerField()
    price = models.PositiveIntegerField()
    description = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created_at',)
    def __str__(self):
        return self.title


class UserSubscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subscription_id = models.ForeignKey(Subscription, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created_at',)
    def __str__(self):
        return self.user.username +'-'+self.subscription_id.title


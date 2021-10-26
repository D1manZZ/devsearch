from .models import Profile
from django.db.models.signals import post_save, post_delete
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings


def user_created(sender, instance, created, **kwargs):
    if created:
        user = instance
        Profile.objects.create(
            user=user,
            name=user.username,
            email=user.email
        )
        send_mail(
            'Welcome message',
            f'Hello, nice to see you, dear {user.username}',
            settings.EMAIL_HOST_USER,
            [user.email],
            fail_silently=False
        )


def profile_deleted(sender, instance, **kwargs):
    profile = instance
    profile.user.delete()


post_save.connect(user_created, sender=User)
post_delete.connect(profile_deleted, sender=Profile)

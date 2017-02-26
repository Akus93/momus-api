from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from momus.models import UserProfile, Comment, Notification, Message, Post


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()


@receiver(post_delete, sender=UserProfile)
def post_delete_user(sender, instance, *args, **kwargs):
    instance.user.delete()


@receiver(post_delete, sender=Comment)
def remove_subcomments(sender, instance, *args, **kwargs):
    for comment in Comment.objects.filter(parent=instance):
        comment.delete()


@receiver(post_save, sender=Comment)
def notify_about_new_comment(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(user=instance.author, type=Notification.COMMENT, data=str(instance.post.slug))


@receiver(post_save, sender=Message)
def notify_about_new_message(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(user=instance.reciver, type=Notification.MESSAGE, data=str(instance.sender))


@receiver(post_delete, sender=Post)
def notify_about_removed_post(sender, instance, *args, **kwargs):
    Notification.objects.create(user=instance.author, type=Notification.REMOVE, data=str(instance.title))










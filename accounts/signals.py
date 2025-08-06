from django.db.models.signals import m2m_changed
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.dispatch import receiver
from django.conf import settings
from blog.models import Post
from django.contrib.auth import get_user_model
from django.contrib.auth.signals import user_logged_in
from allauth.account.signals import user_signed_up

from .models import Profile


User = get_user_model()


@receiver(m2m_changed, sender=User.groups.through)
def assign_reviewer_permissions(sender, instance, action, pk_set, **kwargs):
    if action == "post_add":
        reviewer_group = Group.objects.filter(name="Reviewer").first()
        if reviewer_group and reviewer_group.pk in pk_set:
            content_type = ContentType.objects.get_for_model(Post)
            change_perm = Permission.objects.get(
                codename="change_post", content_type=content_type
            )
            view_perm = Permission.objects.get(
                codename="view_post", content_type=content_type
            )

            instance.user_permissions.add(change_perm, view_perm)


# @receiver(user_logged_in)
@receiver(user_signed_up)
def promote_reader_to_author(sender, request, user, **kwargs):
    try:
        profile = user.profile  # Access the related Profile
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=user)

    if profile.has_paid_author and user.groups.filter(name="Reader").exists():
        reader_group = Group.objects.get(name="Reader")
        author_group, _ = Group.objects.get_or_create(name="Author")
        user.groups.remove(reader_group)
        user.groups.add(author_group)

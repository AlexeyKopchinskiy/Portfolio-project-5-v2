from django.db.models.signals import m2m_changed
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.dispatch import receiver
from django.conf import settings
from blog.models import Post
from django.contrib.auth import get_user_model
from django.contrib.auth.signals import user_logged_in


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


from django.contrib.auth.signals import user_logged_in


@receiver(user_logged_in)
def promote_reader_to_author(sender, request, user, **kwargs):
    reader_group = Group.objects.get(name="Reader")
    author_group, _ = Group.objects.get_or_create(name="Author")

    # If user is in Reader group, promote to Author
    if user.groups.filter(name="Reader").exists():
        user.groups.remove(reader_group)
        user.groups.add(author_group)
        print(f"User {user.username} promoted from Reader to Author.")
    else:
        print(
            f"User {user.username} is already an Author or not in Reader group."
        )

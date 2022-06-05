from django import template
from posts.models import Follow

register = template.Library()


@register.simple_tag()
def following_tags(author, user):
    user_aut = Follow.objects.filter(user=user, author=author)
    if user_aut:
        return True
    else:
        return False

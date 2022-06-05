from django.test import Client
from posts.models import Comment, Follow, Group, Post, User

from .constant import (COUNT_POSTS, TEST_DESCRIPTION, TEST_SLUG, TEST_TEXT,
                       TEST_TITLE, USER_CLIENT, USER_NAME)
from .urls import IMAGE


def fixture_test(cls):
    cls.user = User.objects.create_user(username=USER_NAME)
    cls.group = Group.objects.create(
        title=TEST_TITLE,
        slug=TEST_SLUG,
        description=TEST_DESCRIPTION,
    )
    cls.post = Post.objects.create(
        author=cls.user,
        text=TEST_TEXT,
        group=cls.group,
        image=IMAGE,
    )


def many_posts(cls):
    cls.user = User.objects.create_user(username=USER_NAME)
    cls.group = Group.objects.create(
        title=TEST_TITLE,
        slug=TEST_SLUG,
        description=TEST_DESCRIPTION,
    )
    for i in range(0, COUNT_POSTS):
        cls.post = Post.objects.create(
            author=cls.user,
            text=TEST_TEXT + str(i),
            group=cls.group,
            image=IMAGE,
        )


def tearDown():
    pass


def generalic_class(self, first_object):
    posts_title_0 = first_object.group.title
    posts_slug_0 = first_object.group.slug
    posts_description_0 = first_object.group.description
    posts_author_0 = first_object.author.username
    posts_text_0 = first_object.text
    posts_image_0 = first_object.image

    self.assertEqual(posts_title_0, TEST_TITLE)
    self.assertEqual(posts_slug_0, TEST_SLUG)
    self.assertEqual(posts_description_0, TEST_DESCRIPTION)
    self.assertEqual(posts_text_0, TEST_TEXT)
    self.assertEqual(posts_author_0, USER_NAME)
    self.assertEqual(posts_image_0, IMAGE)


def authorithation(self):
    self.user = User.objects.create_user(username=USER_CLIENT)
    self.authorized_client = Client()
    self.authorized_client.force_login(self.user)


def creat_comment(cls):
    fixture_test(cls)
    cls.comment = Comment.objects.create(
        post=cls.post,
        author=cls.user,
        text=TEST_TEXT,
    )


def creat_follow(cls):
    cls.user = User.objects.create_user(username=USER_NAME)
    cls.author = User.objects.create_user(username=USER_CLIENT)
    cls.follow = Follow.objects.create(
        user=cls.user,
        author=cls.author,
    )

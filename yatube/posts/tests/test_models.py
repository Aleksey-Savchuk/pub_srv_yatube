from django.test import TestCase

from .dics.constant import USER_CLIENT, USER_NAME
from .dics.fixture import creat_comment, creat_follow, fixture_test


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        fixture_test(cls)

    def test_models_have_correct_object_names(self):
        group = PostModelTest.group
        expected_object_name = group.title
        self.assertEqual(expected_object_name, str(group))

    def test_models_have_correct_post(self):
        post = PostModelTest.post
        expected_object_name = post.text[:15]
        self.assertEqual(expected_object_name, str(post))


class CommentModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        creat_comment(cls)

    def test_models_have_correct_post(self):
        comment = CommentModelTest.comment
        expected_object_name = comment.text
        self.assertEqual(expected_object_name, str(comment))


class FollowModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        creat_follow(cls)

    def test_models_have_correct_post(self):
        user = FollowModelTest.follow.user
        author = FollowModelTest.follow.author
        self.assertEqual(USER_NAME, str(user))
        self.assertEqual(USER_CLIENT, str(author))

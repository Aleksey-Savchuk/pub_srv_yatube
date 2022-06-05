from django.test import TestCase
from django.urls import reverse
from posts.models import Comment, Post

from .dics.constant import TEST_TEXT, TEXT_EDIT, USER_CLIENT
from .dics.fixture import authorithation, fixture_test, tearDown
from .dics.urls import COMMENT, CREATE, DETAIL, EDIT, IMAGE, PROFILE


class PostCreateFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        fixture_test(cls)

    def setUp(self):
        authorithation(self)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        tearDown()

    def test_create_post(self):
        post_count = Post.objects.count()
        form_data = {
            'text': TEST_TEXT,
            'group': self.group.pk,
            'image': IMAGE
        }
        response = self.authorized_client.post(
            reverse(CREATE),
            data=form_data,
            follow=True
        )
        self.assertEqual(Post.objects.count(), post_count + 1)
        self.assertRedirects(
            response,
            reverse(PROFILE, kwargs={'username': USER_CLIENT})
        )
        self.assertTrue(
            Post.objects.filter(
                text=TEST_TEXT,
                group=self.group.pk,
                image=IMAGE,
            ).exists()
        )

    def test_edit_post(self):
        form_data = {
            'text': TEXT_EDIT,
            'group': self.group.pk,
            'image': IMAGE,
        }
        response = self.authorized_client.post(
            reverse(EDIT, kwargs={'post_id': self.post.pk}),
            data=form_data,
            follow=True
        )
        self.assertRedirects(response, reverse(
            DETAIL, kwargs={'post_id': self.post.pk})
        )
        self.assertTrue(
            Post.objects.filter(
                text=TEXT_EDIT,
                group=self.group.pk,
                image=IMAGE
            ).exists())


class CommentCreateFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        fixture_test(cls)

    def setUp(self):
        authorithation(self)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        tearDown()

    def test_create_comment(self):
        post_count = Comment.objects.count()
        form_data = {
            'text': TEST_TEXT,
        }

        response = self.authorized_client.post(
            reverse(COMMENT, kwargs={'post_id': self.post.pk}),
            data=form_data,
            follow=True
        )
        self.assertRedirects(response, reverse(
            DETAIL, kwargs={'post_id': self.post.pk})
        )
        self.assertEqual(Comment.objects.count(), post_count + 1)
        self.assertTrue(
            Comment.objects.filter(
                text=TEST_TEXT,
            ).exists()
        )

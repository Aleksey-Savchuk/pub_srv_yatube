from django import forms
from django.conf import settings
from django.core.cache import cache
from django.test import Client, TestCase
from django.urls import reverse
from posts.models import Follow, Post, User

from .dics.constant import (COUNT_POSTS, TEST_SLUG, USER_CLIENT, USER_CLIENT2,
                            USER_NAME)
from .dics.fixture import (authorithation, fixture_test, generalic_class,
                           many_posts, tearDown)
from .dics.page import (CREATE_HTML, DETAIL_HTML, EDIT_HTML, FOLLOW_HTML,
                        GROUP_LIST_HTML, INDEX_HTML, PROFILE_HTML)
from .dics.urls import (CREATE, DETAIL, EDIT, FOLLOW, FOLLOWING, GROUP_LIST,
                        INDEX, PROFILE, UNFOLLOW)


class URLNameSpace(TestCase):
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

    def test_pages_uses_correct_template(self):
        templates_pages_names = {
            INDEX_HTML: reverse(INDEX),
            GROUP_LIST_HTML: reverse(GROUP_LIST, kwargs={'slug': TEST_SLUG}),
            PROFILE_HTML: reverse(PROFILE, kwargs={'username': USER_CLIENT}),
            DETAIL_HTML: reverse(DETAIL, kwargs={'post_id': self.group.pk}),
            CREATE_HTML: reverse(CREATE),
            EDIT_HTML: reverse(EDIT, kwargs={'post_id': self.group.pk}),
            FOLLOW_HTML: reverse(FOLLOW),
        }
        for template, reverse_name in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)


class PostPagesTests(TestCase):
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

    def general_class(self, first_object):
        generalic_class(self, first_object)

    def test_index_page_show_correct_context(self):
        response = self.authorized_client.get(reverse(INDEX))
        first_object = response.context['page_obj'][0]
        self.general_class(first_object)

    def test_group_list_page_show_correct_context(self):
        response = self.authorized_client.get(
            reverse(GROUP_LIST, kwargs={'slug': TEST_SLUG}))
        first_object = response.context['page_obj'][0]
        self.general_class(first_object)

    def test_profile_page_show_correct_context(self):
        response = self.authorized_client.get(
            reverse(PROFILE, kwargs={'username': USER_NAME}))
        first_object = response.context['page_obj'][0]
        self.general_class(first_object)

    def test_post_detail_page_show_correct_context(self):
        response = self.authorized_client.get(
            reverse(DETAIL, kwargs={'post_id': self.group.pk}))
        first_object = response.context['posts']
        self.general_class(first_object)

    def test_post_create_page_show_correct_context(self):
        response = self.authorized_client.get(reverse(CREATE))
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)

    def test_post_edit_page_show_correct_context(self):
        response = self.authorized_client.get(
            reverse(EDIT, kwargs={'post_id': self.group.pk}))
        form_fields = {
            'text': forms.fields.CharField,
            'group': forms.fields.ChoiceField,
            'image': forms.fields.ImageField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)


class PostPaginatorViewsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        many_posts(cls)

    def setUp(self):
        authorithation(self)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        tearDown()

    def test_index_page_contains(self):
        response_pg1 = self.client.get(reverse(INDEX))
        self.assertEqual(len(
            response_pg1.context['page_obj']), settings.POSTS_COUNT)
        response_pg_2 = self.client.get(reverse(INDEX) + '?page=2')
        self.assertEqual(len(
            response_pg_2.context['page_obj']),
            COUNT_POSTS - settings.POSTS_COUNT)

    def test_group_list_page_contains_three_records(self):
        response_pg1 = self.client.get(
            reverse(GROUP_LIST, kwargs={'slug': TEST_SLUG}))
        self.assertEqual(len(
            response_pg1.context['page_obj']), settings.POSTS_COUNT)
        response_pg_2 = self.client.get(
            reverse(GROUP_LIST, kwargs={'slug': TEST_SLUG})
            + '?page=2')
        self.assertEqual(len(
            response_pg_2.context['page_obj']),
            COUNT_POSTS - settings.POSTS_COUNT)

    def test_profil_page_contains_three_records(self):
        response_pg1 = self.client.get(
            reverse(PROFILE, kwargs={'username': USER_NAME}))
        self.assertEqual(len(
            response_pg1.context['page_obj']), settings.POSTS_COUNT)
        response_pg_2 = self.client.get(
            reverse(PROFILE, kwargs={'username': USER_NAME})
            + '?page=2')
        self.assertEqual(len(
            response_pg_2.context['page_obj']),
            COUNT_POSTS - settings.POSTS_COUNT)


class PostAdditionalTest(TestCase):
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

    def general_class(self, first_object):
        generalic_class(self, first_object)

    def test_index_page_show_correct_context(self):
        response = self.authorized_client.get(reverse(INDEX))
        first_object = response.context['page_obj'][0]
        self.general_class(first_object)

    def test_group_list_page_show_correct_context(self):
        response = self.authorized_client.get(
            reverse(GROUP_LIST, kwargs={'slug': TEST_SLUG}))
        first_object = response.context['page_obj'][0]
        self.general_class(first_object)

    def test_profile_page_show_correct_context(self):
        response = self.authorized_client.get(
            reverse(PROFILE, kwargs={'username': USER_NAME}))
        first_object = response.context['page_obj'][0]
        self.general_class(first_object)


class CacheTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        fixture_test(cls)

    def setUp(self):
        authorithation(self)
        self.follow = Follow.objects.create(
            user=self.user,
            author=CacheTests.user,
        )

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        tearDown()

    def test_cache_index_page(self):
        response = self.client.get(reverse(INDEX))
        Post.objects.get(pk=self.post.pk).delete()
        response2 = self.client.get(reverse(INDEX))
        self.assertEqual(response.content, response2.content)
        cache.clear()
        response3 = self.client.get(reverse(INDEX))
        self.assertNotEqual(response2.content, response3.content)

    def test_cache_follow_page(self):
        response = self.authorized_client.get(reverse(FOLLOW))
        Post.objects.get(pk=self.post.pk).delete()
        response2 = self.authorized_client.get(reverse(FOLLOW))
        self.assertEqual(response.content, response2.content)
        cache.clear()
        response3 = self.authorized_client.get(reverse(FOLLOW))
        self.assertNotEqual(response2.content, response3.content)


class FollowAdditionalTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        fixture_test(cls)

    def setUp(self):
        authorithation(self)
        self.follow = Follow.objects.create(
            user=self.user,
            author=FollowAdditionalTest.user,
        )

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        tearDown()

    def general_class(self, first_object):
        generalic_class(self, first_object)

    def test_follow_page_show_correct_context(self):
        response = self.authorized_client.get(reverse(FOLLOW))
        first_object = response.context['page_obj'][0]
        self.general_class(first_object)

    def test_unfollowing_author(self):
        self.authorized_client.get(reverse(
            UNFOLLOW,
            kwargs={'username': FollowAdditionalTest.user}))
        following = FollowAdditionalTest.user
        self.assertIs(
            Follow.objects.filter(user=self.user, author=following).exists(),
            False
        )

    def test_following_author(self):
        self.authorized_client.post(reverse(
            FOLLOWING,
            kwargs={'username': self.user}), follow=True)
        following = FollowAdditionalTest.user
        self.assertIs(
            Follow.objects.filter(user=self.user, author=following).exists(),
            True
        )

    def test_following_login_notauthor(self):
        self.authorized_client.logout()
        self.user = User.objects.create_user(username=USER_CLIENT2)
        self.authorized_client2 = Client()
        self.authorized_client2.force_login(self.user)
        response = self.authorized_client2.get(reverse(FOLLOW))
        first_object = response.context['page_obj']
        self.assertNotIn(
            first_object,
            response.context['page_obj'].object_list
        )


class FollowPaginatorViewsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        many_posts(cls)

    def setUp(self):
        authorithation(self)
        self.follow = Follow.objects.create(
            user=self.user,
            author=FollowPaginatorViewsTest.user,
        )

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        tearDown()

    def test_follow_page_contains(self):
        response_pg1 = self.authorized_client.get(reverse(FOLLOW))
        self.assertEqual(len(
            response_pg1.context['page_obj']), settings.POSTS_COUNT)
        response_pg_2 = self.authorized_client.get(reverse(FOLLOW) + '?page=2')
        self.assertEqual(len(
            response_pg_2.context['page_obj']),
            COUNT_POSTS - settings.POSTS_COUNT)

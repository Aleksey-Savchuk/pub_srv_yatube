from http import HTTPStatus

from django.test import Client, TestCase

from .dics.constant import TEST_SLUG
from .dics.fixture import authorithation, fixture_test, tearDown
from .dics.page import (CREATE_HTML, DETAIL_HTML, EDIT_HTML, FOLLOW_HTML,
                        GROUP_LIST_HTML, INDEX_HTML, PROFILE_HTML)


class StaticURLTests(TestCase):
    def setUp(self):
        self.guest_client = Client()

    def test_author(self):
        response = self.guest_client.get('/about/author/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_tech(self):
        response = self.guest_client.get('/about/tech/')
        self.assertEqual(response.status_code, HTTPStatus.OK)


class PostURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        fixture_test(cls)

    def setUp(self):
        self.guest_client = Client()
        authorithation(self)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        tearDown()

    def test_index_url(self):
        response = self.guest_client.get('/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_group_url(self):
        response = self.guest_client.get('/group/' + TEST_SLUG + '/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_profile_url_user_name(self):
        user_profile = self.user
        response = self.authorized_client.get('/profile/' + str(user_profile),
                                              follow=True)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_post_id_url(self):
        response = self.guest_client.get(
            '/posts/' + str(self.group.pk) + '/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_post_id_author_url(self):
        response = self.authorized_client.get(
            '/posts/' + str(self.group.pk) + '/edit/', follow=True)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_post_create_url(self):
        response = self.authorized_client.get('/create/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_post_id_404_url(self):
        response = self.guest_client.get('/unexisting/')
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_urls_uses_correct_template(self):
        templates_url_names = {
            INDEX_HTML: '/',
            GROUP_LIST_HTML: '/group/' + TEST_SLUG + '/',
            PROFILE_HTML: '/profile/' + str(self.user) + '/',
            DETAIL_HTML: '/posts/' + str(self.group.pk) + '/',
            CREATE_HTML: '/posts/' + str(self.group.pk) + '/edit/',
            EDIT_HTML: '/create/',
        }
        for template, address in templates_url_names.items():
            with self.subTest(address=address):
                response = self.authorized_client.get(address)
                self.assertTemplateUsed(response, template)


class FollowURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        fixture_test(cls)

    def setUp(self):
        self.guest_client = Client()
        authorithation(self)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        tearDown()

    def test_follow_index_url(self):
        response = self.authorized_client.get('/follow/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_urls_uses_correct_template(self):
        templates_url_names = {
            FOLLOW_HTML: '/follow/'
        }
        for template, address in templates_url_names.items():
            with self.subTest(address=address):
                response = self.authorized_client.get(address)
                self.assertTemplateUsed(response, template)

from django.test import TestCase, Client
from django.urls import reverse
from .models import Homepage
from news.models import User

# Create your tests here.

class HomepageModelTest(TestCase):
    def setUp(self):
        self.homepage = Homepage.objects.create()

    def test_homepage_str(self):
        self.assertIsInstance(str(self.homepage), str)

class CMSDashboardViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')

    def test_dashboard_requires_login(self):
        response = self.client.get(reverse('cms_dashboard'))
        self.assertEqual(response.status_code, 302)  # Should redirect to login
        self.assertIn('/login', response.url)

    def test_dashboard_logged_in(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('cms_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Dashboard')

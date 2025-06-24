from django.test import TestCase, Client
from django.urls import reverse
from .models import Article, Author, Image, Section, User
from django.utils import timezone

# Create your tests here.

class ArticleModelTest(TestCase):
    def setUp(self):
        section = Section.objects.create(section_name="Test Section")
        author = Author.objects.create(byline="Test Author", author_bio="Bio", pic=None)
        image = Image.objects.create(name="Test Image", image="media/news/images/test.jpg")
        self.article = Article.objects.create(
            headline="Test Headline",
            main=image,
            byline=author,
            deck="Test Deck",
            slug="test-slug",
            date=timezone.now(),
            content="Test Content",
            section=section,
            is_published=True
        )

    def test_article_str(self):
        self.assertIn(self.article.headline, str(self.article))
        self.assertIn(str(self.article.byline), str(self.article))

class NewsViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_homepage_status_code(self):
        response = self.client.get(reverse('news:homepage'))
        self.assertIn(response.status_code, [200, 302])  # Accept 302 if homepage redirects

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils import timezone
from django.db import IntegrityError
from django.core.exceptions import ValidationError

from .models import (
    Profile, Subsection, Section, Image, Author, 
    Article, Comment, Following, Like
)

User = get_user_model()

class UserModelTest(TestCase):
    def test_user_creation(self):
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'test@example.com')
        self.assertTrue(user.check_password('testpass123'))

class SectionModelTest(TestCase):
    def test_section_creation(self):
        section = Section.objects.create(section_name='Test Section')
        self.assertEqual(str(section), 'Test Section')

class AuthorModelTest(TestCase):
    def setUp(self):  # Changed from test_setUp to setUp
        self.image_file = SimpleUploadedFile(
            name='author_pic.jpg',
            content=b'fake image content',
            content_type='image/jpeg'
        )
        self.pic = Image.objects.create(
            name='Author Picture',
            image=self.image_file
        )

    def test_author_creation(self):
        author = Author.objects.create(
            byline='Test Author',
            author_bio='<p>Test bio</p>',
            pic=self.pic
        )
        self.assertEqual(str(author), 'Test Author')

class ArticleModelTest(TestCase):
    def setUp(self):  # Changed from test_setUp to setUp
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.section = Section.objects.create(section_name='Test Section')
        
        # Create a proper image file for testing
        self.image_file = SimpleUploadedFile(
            name='test_image.jpg',
            content=b'fake image content',
            content_type='image/jpeg'
        )
        self.image = Image.objects.create(
            name='Test Image',
            image=self.image_file
        )
        
        self.author = Author.objects.create(
            byline='Test Author',
            author_bio='<p>Test author bio</p>'
        )

    def test_article_creation(self):
        article = Article.objects.create(
            headline='Test Headline',
            main=self.image,
            byline=self.author,
            deck='Test deck content',
            slug='test-headline',
            date=timezone.now(),
            content='<p>Test article content</p>',
            section=self.section,
            changed_by=self.user,
            is_published=True
        )
        self.assertEqual(str(article), f'Test Headline by {self.author}')
        self.assertTrue(article.is_published)

class CommentModelTest(TestCase):
    def setUp(self):  
        self.user = User.objects.create_user(  
            username='commenter', 
            password='testpass123'
        )
        self.author = Author.objects.create(
            byline='Article Author',
            author_bio='<p>Test bio</p>'
        )
        self.article = Article.objects.create(
            headline='Test Article',
            byline=self.author,
            deck='Test deck',
            slug='test-article',
            content='<p>Article content</p>'
        )

    def test_comment_creation(self):
        comment = Comment.objects.create(
            commenter=self.user,
            comment_text='This is a test comment',
            article=self.article
        )
        self.assertEqual(comment.commenter, self.user)
        self.assertEqual(comment.article, self.article)

class LikeModelTest(TestCase):
    def setUp(self):
        self.liker = User.objects.create_user(username='liker', password='testpass123')
        self.commenter = User.objects.create_user(username='commenter', password='testpass123')
        self.author = Author.objects.create(
            byline='Article Author',
            author_bio='<p>Test bio</p>'
        )
        self.article = Article.objects.create(
            headline='Test Article',
            byline=self.author,
            deck='Test deck',
            slug='test-article',
            content='<p>Article content</p>'
        )
        self.comment = Comment.objects.create(
            commenter=self.commenter,
            comment_text='Test comment',
            article=self.article
        )

    def test_like_creation(self):
        like = Like.objects.create(
            liker=self.liker,
            comment_liked=self.comment
        )
        self.assertEqual(like.liker, self.liker)
        self.assertEqual(like.comment_liked, self.comment)
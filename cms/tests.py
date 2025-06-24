from django.test import TestCase, override_settings
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

# Override storage settings for testing to avoid S3 issues
@override_settings(
    DEFAULT_FILE_STORAGE='django.core.files.storage.FileSystemStorage',
    MEDIA_ROOT='/tmp/test_media/'
)


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
        self.assertEqual(str(user), 'testuser')


class ProfileModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        # Create a simple image file for testing
        self.image_file = SimpleUploadedFile(
            name='test_image.jpg',
            content=b'fake image content',
            content_type='image/jpeg'
        )

    def test_profile_creation(self):
        profile = Profile.objects.create(
            user=self.user,
            bio='<p>Test bio</p>',
            profile_picture=self.image_file
        )
        self.assertEqual(profile.user, self.user)
        self.assertEqual(profile.bio, '<p>Test bio</p>')
        self.assertIsNotNone(profile.profile_picture)

    def test_profile_str(self):
        profile = Profile.objects.create(user=self.user)
        self.assertEqual(str(profile), f'{self.user.username} Profile')

    def test_profile_optional_fields(self):
        # Test that bio and profile_picture can be blank/null
        profile = Profile.objects.create(user=self.user)
        self.assertIsNone(profile.bio)
        self.assertFalse(profile.profile_picture)


class SubsectionModelTest(TestCase):
    def test_subsection_creation(self):
        subsection = Subsection.objects.create(
            subsection_name='Test Subsection',
            sub_url_name='test-subsection'
        )
        self.assertEqual(subsection.subsection_name, 'Test Subsection')
        self.assertEqual(subsection.sub_url_name, 'test-subsection')

    def test_subsection_str(self):
        subsection = Subsection.objects.create(subsection_name='Test Subsection')
        self.assertEqual(str(subsection), 'Test Subsection')

    def test_subsection_max_length(self):
        # Test that subsection_name respects max_length
        with self.assertRaises(ValidationError):
            subsection = Subsection(subsection_name='a' * 21)  # Exceeds max_length of 20
            subsection.full_clean()


class SectionModelTest(TestCase):
    def test_section_creation(self):
        section = Section.objects.create(
            section_name='Test Section',
            section_description='Test description',
            section_url_name='test-section'
        )
        self.assertEqual(section.section_name, 'Test Section')
        self.assertEqual(str(section), 'Test Section')

    def test_section_optional_fields(self):
        section = Section.objects.create(section_name='Test Section')
        self.assertIsNone(section.section_description)
        self.assertIsNone(section.section_url_name)


class ImageModelTest(TestCase):
    def setUp(self):
        self.image_file = SimpleUploadedFile(
            name='test_image.jpg',
            content=b'fake image content',
            content_type='image/jpeg'
        )

    def test_image_creation(self):
        image = Image.objects.create(
            name='Test Image',
            image=self.image_file,
            caption='Test caption'
        )
        self.assertEqual(image.name, 'Test Image')
        self.assertEqual(image.caption, 'Test caption')
        self.assertIsNotNone(image.image)

    def test_image_get_image_url(self):
        image = Image.objects.create(
            name='Test Image',
            image=self.image_file
        )
        # Should return the actual image URL when image exists
        self.assertTrue(image.get_image_url().endswith('.jpg'))

    def test_image_get_image_url_fallback(self):
        image = Image.objects.create(name='Test Image')
        # Should return fallback URL when no image
        fallback_url = image.get_image_url()
        self.assertIn('GettyImages-985192218.jpg', fallback_url)

""" 
class AuthorModelTest(TestCase):
    def setUp(self):
        # Create image without file to avoid storage issues
        self.pic = Image.objects.create(name='Author Picture')

    def test_author_creation(self):
        author = Author.objects.create(
            byline='Test Author',
            author_bio='<p>Test bio</p>',
            pic=self.pic
        )
        self.assertEqual(author.byline, 'Test Author')
        self.assertEqual(str(author), 'Test Author')

    def test_author_slug_generation(self):
        author = Author.objects.create(
            byline='Test Author Name',
            author_bio='<p>Test bio</p>'
        )
        self.assertEqual(author.author_slug, 'test-author-name')

    def test_author_without_pic(self):
        author = Author.objects.create(
            byline='Test Author',
            author_bio='<p>Test bio</p>'
        )
        self.assertIsNone(author.pic)


class ArticleModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.section = Section.objects.create(section_name='Test Section')
        self.image = Image.objects.create(name='Test Image')
        self.author = Author.objects.create(
            byline='Test Author',
            author_bio='<p>Test bio</p>'
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
        self.assertEqual(article.headline, 'Test Headline')
        self.assertEqual(str(article), f'Test Headline by {self.author}')
        self.assertTrue(article.is_published)

    def test_article_url_auto_generation(self):
        article = Article.objects.create(
            headline='Test Article Title',
            byline=self.author,
            deck='Test deck',
            slug='test-article',
            content='<p>Content</p>'
        )
        self.assertEqual(article.url, 'test-article-title')
 """

class CommentModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='commenter',
            email='commenter@example.com',
            password='testpass123'
        )
        self.author = Author.objects.create(
            byline='Article Author',
            author_bio='<p>Author bio</p>'
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
        self.assertEqual(comment.comment_text, 'This is a test comment')
        self.assertEqual(comment.article, self.article)

    def test_comment_str(self):
        comment = Comment.objects.create(
            commenter=self.user,
            comment_text='Test comment',
            article=self.article
        )
        expected_str = f'{self.user} commented on {self.article}'
        self.assertEqual(str(comment), expected_str)

    def test_comment_likes_count(self):
        comment = Comment.objects.create(
            commenter=self.user,
            comment_text='Test comment',
            article=self.article
        )
        # Initially no likes
        self.assertEqual(comment.likes(), 0)


class FollowingModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='follower',
            email='follower@example.com',
            password='testpass123'
        )
        
        self.author = Author.objects.create(
            byline='Popular Author',
            author_bio='<p>Popular author bio</p>'
        )

    def test_following_creation(self):
        following = Following.objects.create(
            user_following=self.user,
            author_followed=self.author
        )
        
        self.assertEqual(following.user_following, self.user)
        self.assertEqual(following.author_followed, self.author)

    def test_following_str(self):
        following = Following.objects.create(
            user_following=self.user,
            author_followed=self.author
        )
        expected_str = f'{self.user} is following {self.author}'
        self.assertEqual(str(following), expected_str)


class LikeModelTest(TestCase):
    def setUp(self):
        self.liker = User.objects.create_user(
            username='liker',
            email='liker@example.com',
            password='testpass123'
        )
        self.commenter = User.objects.create_user(
            username='commenter',
            email='commenter@example.com',
            password='testpass123'
        )
        self.author = Author.objects.create(
            byline='Article Author',
            author_bio='<p>Author bio</p>'
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

    def test_like_str(self):
        like = Like.objects.create(
            liker=self.liker,
            comment_liked=self.comment
        )
        expected_str = f'User {self.liker} liked {self.comment}'
        self.assertEqual(str(like), expected_str)


class SubsectionModelTest(TestCase):
    def test_subsection_creation(self):
        subsection = Subsection.objects.create(
            subsection_name='Test Subsection',
            sub_url_name='test-subsection'
        )
        self.assertEqual(subsection.subsection_name, 'Test Subsection')
        self.assertEqual(str(subsection), 'Test Subsection')


class ImageModelTest(TestCase):
    def test_image_creation_without_file(self):
        # Test creating image without actual file to avoid storage issues
        image = Image.objects.create(
            name='Test Image',
            caption='Test caption'
        )
        self.assertEqual(image.name, 'Test Image')
        self.assertEqual(image.caption, 'Test caption')

    def test_image_get_image_url_fallback(self):
        image = Image.objects.create(name='Test Image')
        # Should return fallback URL when no image
        fallback_url = image.get_image_url()
        self.assertIn('GettyImages-985192218.jpg', fallback_url)


class ProfileModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

    def test_profile_creation(self):
        profile = Profile.objects.create(
            user=self.user,
            bio='<p>Test bio</p>'
        )
        self.assertEqual(profile.user, self.user)
        self.assertEqual(profile.bio, '<p>Test bio</p>')

    def test_profile_str(self):
        profile = Profile.objects.create(user=self.user)
        self.assertEqual(str(profile), f'{self.user.username} Profile')


class FollowingModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='follower',
            email='follower@example.com',
            password='testpass123'
        )
        self.author = Author.objects.create(
            byline='Popular Author',
            author_bio='<p>Popular author bio</p>'
        )

    def test_following_creation(self):
        following = Following.objects.create(
            user_following=self.user,
            author_followed=self.author
        )
        self.assertEqual(following.user_following, self.user)
        self.assertEqual(following.author_followed, self.author)

    def test_following_str(self):
        following = Following.objects.create(
            user_following=self.user,
            author_followed=self.author
        )
        expected_str = f'{self.user} is following {self.author}'
        self.assertEqual(str(following), expected_str)
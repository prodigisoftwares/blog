from django.test import TestCase
from django.utils import timezone
from django.utils.text import slugify

from ..models import Category, Post


class CategoryModelTest(TestCase):
    """Test Category model functionality."""

    def test_category_creation(self):
        """Test that a category can be created with proper slug generation."""
        category = Category.objects.create(
            name="Test Category", description="A test category description"
        )
        self.assertEqual(category.name, "Test Category")
        self.assertEqual(category.slug, slugify("Test Category"))
        self.assertEqual(str(category), "Test Category")

    def test_category_slug_uniqueness(self):
        """Test that category slugs must be unique."""
        Category.objects.create(name="Test Category")
        with self.assertRaises(Exception):  # IntegrityError
            Category.objects.create(name="Test Category")


class PostModelTest(TestCase):
    """Test Post model functionality."""

    def setUp(self):
        """Set up test data."""
        self.category = Category.objects.create(name="Test Category")

    def test_post_creation(self):
        """Test that a post can be created with proper slug generation."""
        post = Post.objects.create(
            title="Test Post Title",
            content="This is test content for the post.",
            category=self.category,
            is_published=True,
            published_at=timezone.now(),
        )
        self.assertEqual(post.title, "Test Post Title")
        self.assertEqual(post.slug, slugify("Test Post Title"))
        self.assertEqual(str(post), "Test Post Title")
        self.assertTrue(post.is_visible)

    def test_post_slug_uniqueness(self):
        """Test that post slugs must be unique."""
        Post.objects.create(title="Test Post")
        with self.assertRaises(Exception):  # IntegrityError
            Post.objects.create(title="Test Post")

    def test_unpublished_post_not_visible(self):
        """Test that unpublished posts are not visible."""
        post = Post.objects.create(
            title="Unpublished Post", content="Content", is_published=False
        )
        self.assertFalse(post.is_visible)

    def test_get_absolute_url(self):
        """Test that posts have correct absolute URLs."""
        post = Post.objects.create(
            title="URL Test Post",
            content="Content",
            is_published=True,
            published_at=timezone.now(),
        )
        expected_url = f"/{post.slug}/"
        self.assertEqual(post.get_absolute_url(), expected_url)

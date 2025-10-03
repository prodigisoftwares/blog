from django.views.generic import DetailView, ListView

from ..models import Post


class PostListView(ListView):
    """Display list of published blog posts."""

    model = Post
    template_name = "posts/post_list.html"
    context_object_name = "posts"
    paginate_by = 10

    def get_queryset(self):  # pragma: no cover
        return Post.objects.filter(
            is_published=True, published_at__isnull=False
        ).order_by("-published_at")


class PostDetailView(DetailView):
    """Display individual blog post."""

    model = Post
    template_name = "posts/post_detail.html"
    context_object_name = "post"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_queryset(self):  # pragma: no cover
        return Post.objects.filter(is_published=True, published_at__isnull=False)

from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from django.views.generic.base import View

from .models import Post, Magazine
from .forms import ReviewForm
from django.contrib.auth.models import User


def home(request):
    return render(request, 'home.html', {})

class PostView(ListView):
    """Список постов"""
    model = Post
    queryset = Post.objects.filter(draft=False)
    #template_name = "posts/post_list.html"


class PostDetailView(DetailView):
    """Полное описание фильма"""
    model = Post
    slug_field = 'url'
    #template_name = "posts/post_detail.html"


class AddReview(View):
    """Отзывы"""
    def post(self, request, pk):
        form = ReviewForm(request.POST)
        posting = Post.objects.get(id=pk)
        if form.is_valid():
            form = form.save(commit=False)
            if request.POST.get("parent", None):
                form.parent_id = int(request.POST.get("parent"))
            form.post = posting
            form.save()
        return redirect(posting.get_absolute_url())


class MagazinePostListView(ListView):
    model = Post
    template_name = 'post/magazine_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 5
    # queryset = Post.objects.filter(draft=False)

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(magazine__market=user)

    # order_by('-date_posted')


class MagazineView(DetailView):
    """Полное описание фильма"""
    model = Magazine
    context_object_name = 'mpost'
    slug_field = 'market__username'
    template_name = "market/market_detail.html"

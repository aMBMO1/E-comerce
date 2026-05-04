from django.urls import reverse_lazy
from django.utils.text import slugify
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post
from .forms import PostForm


class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Post.objects.filter(
                Q(status=1) | Q(author=self.request.user)
            ).distinct()
        return Post.objects.filter(status=1)


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Post.objects.filter(
                Q(status=1) | Q(author=self.request.user)
            ).distinct()
        return Post.objects.filter(status=1)


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy('post_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.slug = slugify(form.instance.title)

        base_slug = form.instance.slug
        counter = 1
        while Post.objects.filter(slug=form.instance.slug).exists():
            form.instance.slug = f"{base_slug}-{counter}"
            counter += 1

        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy('post_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.slug = slugify(form.instance.title)

        base_slug = form.instance.slug
        counter = 1
        while Post.objects.filter(slug=form.instance.slug).exclude(pk=self.object.pk).exists():
            form.instance.slug = f"{base_slug}-{counter}"
            counter += 1

        return super().form_valid(form)


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('post_list')
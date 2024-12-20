from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView, ListView

from blog.models import BlogPost


# Create your views here.
class BlogPostCreateView(CreateView):
    model = BlogPost
    fields = ("title", "content", "preview", "publication_sign", "number_of_views")
    success_url = reverse_lazy('blog:blogpost_list')


class BlogPostDetailView(DetailView):
    model = BlogPost
    template_name = 'blog/blogpost_detail.html'
    context_object_name = 'post_detail'
    success_url = reverse_lazy('blog:blogpost_list')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.number_of_views += 1
        self.object.save()
        return self.object


class BlogPostUpdateView(UpdateView):
    model = BlogPost
    fields = ("title", "content", "preview", "publication_sign", "number_of_views")
    template_name = 'blog/blogpost_form.html'
    success_url = reverse_lazy('blog:blogpost_list')

    def get_success_url(self):
        return reverse('blog:blogpost_detail', args=[self.kwargs.get('pk')])


class BlogPostDeleteView(DeleteView):
    model = BlogPost
    template_name = 'blog/blogpost_confirm_delete.html'
    success_url = reverse_lazy('blog:blogpost_list')


class BlogPostListView(ListView):
    model = BlogPost
    template_name = 'blog/blogpost_list.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return BlogPost.objects.filter(publication_sign=True)


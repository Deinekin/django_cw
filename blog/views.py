from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse

from blog.models import Blog


class BlogCreateView(CreateView):
    model = Blog
    fields = ('title', 'content')

    success_url = reverse_lazy('blog:view_all_blogs')


class BlogDetailView(DetailView):
    model = Blog

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.quantity_of_views += 1
        self.object.save()
        return self.object


class BlogListView(ListView):
    model = Blog

    def get_queryset(self):
        return Blog.objects.all()


class BlogUpdateView(UpdateView):
    model = Blog
    fields = ('title', 'content')

    success_url = reverse_lazy('blog:view_all_blogs')


class BlogDeleteView(DeleteView):
    model = Blog

    success_url = reverse_lazy('blog:view_all_blogs')

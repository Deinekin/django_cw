from django.urls import path
from django.views.decorators.cache import cache_page
from blog.apps import BlogConfig
from blog.views import BlogCreateView, BlogDeleteView, BlogDetailView, BlogUpdateView, BlogListView

app_name = BlogConfig.name

urlpatterns = [
    path('create_blog/', BlogCreateView.as_view(), name='create_blog'),
    path('', cache_page(60)(BlogListView.as_view()), name='view_all_blogs'),
    path('blog-<int:pk>/', BlogDetailView.as_view(), name='view_blog'),
    path('blog/edit/<int:pk>/', BlogUpdateView.as_view(), name='edit_blog'),
    path('blog/delete/<int:pk>/', BlogDeleteView.as_view(), name='delete_blog'),
]

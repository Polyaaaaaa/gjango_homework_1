from django.urls import path

from .views import (BlogPostCreateView, BlogPostDeleteView, BlogPostDetailView,
                    BlogPostListView, BlogPostUpdateView)

app_name = "blog"

urlpatterns = [
    path("", BlogPostListView.as_view(), name="blogpost_list"),
    path("create/", BlogPostCreateView.as_view(), name="blogpost_create"),
    path("detail/<int:pk>/", BlogPostDetailView.as_view(), name="blogpost_detail"),
    path("update/<int:pk>/", BlogPostUpdateView.as_view(), name="blogpost_update"),
    path("delete/<int:pk>/", BlogPostDeleteView.as_view(), name="blogpost_delete"),
]

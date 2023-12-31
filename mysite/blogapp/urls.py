from django.urls import path
from .views import ArticleDetailView, ArticlesListView, LatestArticlesFeed

app_name = 'blogapp'

urlpatterns = [
    path('articles/', ArticlesListView.as_view(), name='articles'),
    path('articles/<int:pk>/', ArticleDetailView.as_view(), name='article_details'),
    path('articles/latest/feed/', LatestArticlesFeed, name='articles_feed'),
]

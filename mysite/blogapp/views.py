from django.contrib.syndication.views import Feed
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView

from .models import Article


class ArticlesListView(ListView):
    queryset = (Article.objects.filter(published_at__isnull=False).order_by('-published_at'))


class ArticleDetailView(DetailView):
    model = Article


class LatestArticlesFeed(Feed):
    title = 'Blog articles (latest)'
    description = 'Updates on changes and addition blog articles'
    link = reverse_lazy('blogapp:articles')

    # создание метода для возвращения статей для RSS ленты
    def items(self):
        return Article.objects.filter(published_at__isnull=False).order_by('-published_at')[:]

    # создание метода для получения заголовка из объекта в списке статей
    def item_title(self, item: Article):
        return item.title

    # создание метода, где будет информация об объекте, о котором вышла статья
    def item_description(self, item: Article):
        return item.body[:200]

    # создание метода, чтобы пользователь мог перейти на мой сайт
    def item_link(self, item: Article):
        return reverse('blogapp:article_details', kwargs={'pk': item.pk})


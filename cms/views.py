from django.shortcuts import render

from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from news.models import Article, User, Image, Author, Section
from .forms import ArticleForm


# Create your views here.
def cms_dashboard(request):
    articles = Article.objects.all()
    return render(request, 'cms/dashboard.html', {
      'articles': articles
      })

def cms_create_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect(reverse('cms_dashboard'))
    else:
        form = ArticleForm()
    return render(request, 'cms/cms_article.html', {
        'form': form
        })

def cms_edit_article(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            form.save()
            return redirect(reverse('cms_dashboard'))
    else:
        form = ArticleForm(instance=article)
    return render(request, 'cms/article_form.html', {
        'form': form
        })

def cms_delete_article(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    if request.method == 'POST':
        article.delete()
        return redirect(reverse('cms_dashboard'))
    return render(request, 'cms/article_confirm_delete.html', {
        'article': article
        })
from django.shortcuts import render
import json
import requests
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.http import JsonResponse
from django.contrib.staticfiles.apps import StaticFilesConfig

from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from news.models import Article, User, Image, Author, Section, User
from .models import Homepage
from .forms import ArticleForm, HomepageForm
from django.db.models import Q
from django.core.paginator import Paginator


# Create your views here.


def cms_dashboard(request):
    search_article = request.GET.get('q')
    if search_article:
        return search(request, search_article)
    articles = Article.objects.all()
    return render(request, 'cms/dashboard.html', {
      'articles': articles
      })

def create_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('cms_dashboard'))
    else:
        form = ArticleForm()
    return render(request, 'cms/article.html', {
        'form': form
        })

def edit_article(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('cms_dashboard'))
    else:
        form = ArticleForm(instance=article)
    return render(request, 'cms/article.html', {
        'form': form
        })

def search(request, query):
    search_results = Article.objects.filter(Q(headline__icontains=query) | Q(content__icontains=query))
    articles = Paginator(search_results, 10)
    page_number = request.GET.get("page")
    page_obj = articles.get_page(page_number)
    return render(request, "cms/search.html",{
        "search_results":search_results,
        "query":query,
        "page_obj":page_obj
    })

def edit_homepage(request):
    if request.method == 'POST':
        form = HomepageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('cms_dashboard'))
    else:
        form = HomepageForm()
    return render(request, 'cms/edit.html', {
        'form': form
        })


def delete_article(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    if request.method == 'POST':
        article.delete()
        return HttpResponseRedirect(reverse('cms_dashboard'))
    return render(request, 'cms/article_confirm_delete.html', {
        'article': article
        })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("cms_dashboard"))
        else:
            return render(request, "cms/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "cms/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("cms_dashboard"))


def register(request):
    return redirect(reverse('cms_dashboard'))
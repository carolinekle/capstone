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
from .forms import ArticleForm, HomepageForm, AuthorForm, ImageForm, SectionForm
from django.db.models import Q
from django.core.paginator import Paginator
from haystack.query import SearchQuerySet
from simple_history.models import HistoricalRecords

# Create your views here.

#index
def cms_dashboard(request):       
    articles = Article.objects.order_by("-date")
    return render(request, 'cms/dashboard.html', {
      'articles': articles
      })

#article
def create_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            history = form.history.all()
            return HttpResponseRedirect(reverse('cms_dashboard'))
        else:
            return render(request, 'cms/error_page.html')
    else:
        form = ArticleForm()
    return render(request, 'cms/article.html', {
        'form': form,
    })

def edit_article(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    history = article.history.all()
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('cms_dashboard'))
    else:
        form = ArticleForm(instance=article)
    return render(request, 'cms/article.html', {
        'article':article,
        'history':history,
        'form': form,
        'image_url':article.main.get_image_url()
        })

#author
def create_author(request):
    if request.method == 'POST':
        image_form = ImageForm(request.POST, request.FILES )
        form = AuthorForm(request.POST, request.FILES)
        if form.is_valid and image_form.is_valid():
            form.save()
            image_form.save()
            return HttpResponseRedirect(reverse('cms_dashboard'))
    else:
        form = AuthorForm()
        image_form = ImageForm()
    return render(request, 'cms/author_page.html', {
        'form': form,
        'image_form':image_form
        })

def edit_author(request, author_id):
    author = get_object_or_404(Author, id=author_id)
    if request.method == 'POST':
        form = AuthorForm(request.POST, request.FILES, instance=author)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('cms_dashboard'))
    else:
        form = AuthorForm(instance=author)
    return render(request, 'cms/author_page.html',{
        'form':form
    })

#image
def create_image(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('cms_dashboard'))
    else:
        form = ImageForm()
    return render(request, 'cms/create_image.html', {
        'form': form,
    })

def edit_image(request, image_id):
    image = get_object_or_404(Image, id=image_id)
    if request.method =="POST":
        form = ImageForm(request.POST, request.FILES, instance=image)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('cms_dashboard'))
    else:
        form = ImageForm(instance=image)
    return render(request, 'cms/create_image.html', {
        'form': form
        })

#get image url
def get_image_url(request, image_id): 
    image = get_object_or_404(Image, id=image_id)
    url = image.get_image_url()
    print(url)
    return JsonResponse({'image_url': url})

#section
def create_section(request):
    if request.method == 'POST':
        form = SectionForm(request.POST, request.FILES)
        if form.is_valid:
            form.save()
            return HttpResponseRedirect(reverse('cms_dashboard'))
    else:
        form = SectionForm()
    return render(request, 'cms/section.html', {
        'form': form,
        })

def edit_section(request, section_id):
    section = get_object_or_404(Section, id=section_id)
    if request.method =="POST":
        form = SectionForm(request.POST, request.FILES, instance=section)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('cms_dashboard'))
    else:
        form = SectionForm(instance=section)
    return render(request, 'cms/section.html', {
        'form': form
        })

#homepage
def edit_homepage(request):
    if request.method == 'POST':
        form = HomepageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('cms_dashboard'))
    else:
        form = HomepageForm()
    return render(request, 'cms/edit_homepage.html', {
        'form': form
        })

#search
def get_query(request):
    search_content = request.GET.get('q')
    if search_content:
        return search(request, search_content)

def search(request, query):
    search_results = SearchQuerySet().filter(content=query)
    return render(request, 'cms/search.html', {
        "search_results": search_results,
        "search_q":query
        })

#delete
def delete_article(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    if request.method == 'POST':
        article.delete()
        return HttpResponseRedirect(reverse('cms_dashboard'))
    return render(request, 'cms/article_confirm_delete.html', {
        'article': article
        })

#user
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
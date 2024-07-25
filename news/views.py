import json
import requests
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.http import JsonResponse
from django.contrib.staticfiles.apps import StaticFilesConfig

from newsapi import NewsApiClient

from .models import User, Section, Article, Author, Comment, Image
# Create your views here.

newsapi = NewsApiClient(api_key='os.getenv(API_KEY)')

def index(request):
    all_articles = Article.objects.order_by('-date').all()
    all_sections = Section.objects.all()
    hero_articles = Article.objects.filter(is_hero=True).order_by('hero_priority')  
    return render(request, "news/homepage.html", {
        "all_articles" : all_articles,
        "all_sections": all_sections,
        "hero_articles":hero_articles
    })


def fetch_news(query, language='en', page_size=5):
    url = 'https://newsapi.org/v2/everything'
    params = {
        'q': query,
        'language': language,
        'pageSize': page_size,
        'apiKey': settings.NEWS_API_KEY
    }
    response = requests.get(url, params=params)
    data = response.json()
    return data

def load_news(request):
    query = 'technology'  
    news_data = fetch_news(query)
    news_articles = news_data.get('articles', [])
    return render(request, 'news/news.html', {
        'news_articles': news_articles
        })

def page_not_found(request):
    return
def electric_drama(request):
    return

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("homepage"))
        else:
            return render(request, "news/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "news/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("homepage"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "news/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "news/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("homepage"))
    else:
        return render(request, "news/register.html")
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
from django.core.paginator import Paginator
from django.db.models import Q


from newsapi import NewsApiClient

from .models import User, Section, Article, Author, Comment, Image, Following
# Create your views here.

newsapi = NewsApiClient(api_key='f14129816c0d44ad9387564f2e4dec69')

def index(request):
    search_article = request.GET.get('search')
    if search_article:
        return search(request, search_article)

    all_articles = Article.objects.filter(is_published=True, is_hero=False).order_by('-date').all()
    all_sections = Section.objects.all()
    hero_articles = Article.objects.filter(is_hero=True)
    return render(request, "news/homepage.html", {
        "all_articles" : all_articles,
        "all_sections": all_sections,
        "hero_articles": hero_articles
    })

def article_details(request, section_url_name, url):
    section = get_object_or_404(Section, section_url_name=section_url_name)
    article = get_object_or_404(Article, url=url, section=section)
    comments= Comment.objects.filter(article=article)
    return render(request, "news/article.html", {
        "article": article,
        "section": section,
        "comments":comments
    })

def comment(request, article_id):
    this_commenter = request.user
    text = request.POST["new_comment"]
    this_article= Article.objects.get(id=article_id)

    new_comment = Comment(
        comment_text=text,
        commenter=this_commenter,
        listing=this_article
    )
    new_comment.save()
    return HttpResponseRedirect(reverse("article.html", args=[article_id]))

def section(request, section_url_name):
    if section_url_name == "news":
        return load_news(request)
    else: 
        section = get_object_or_404(Section, section_url_name=section_url_name)
        section_articles = Article.objects.filter(section=section)
        articles = Paginator(section_articles, 10)
        page_number = request.GET.get("page")
        page_obj = articles.get_page(page_number)

        return render(request, "news/section-front.html",{
            "section":section,
            "section_articles":section_articles,
            "page_obj":page_obj
        })

def author_page(request, author_slug):
    author = get_object_or_404(Author, author_slug=author_slug)
    author_articles =Article.objects.filter(byline=author)
    articles = Paginator(author_articles, 10)
    page_number = request.GET.get("page")
    page_obj = articles.get_page(page_number)

    return render(request, "news/author.html",{
        "author":author,
        "author_articles":author_articles,
        "page_obj":page_obj
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

def profile(request, user_username):
   user = get_object_or_404(User, username=user_username)
   followed_authors = Following.objects.filter(user_following=user).values_list('author_followed', flat=True)
   articles_by_followed_authors = Article.objects.filter(byline__in=followed_authors)
   
   articles = Paginator(articles_by_followed_authors, 10)
   page_number = request.GET.get("page")
   page_obj = articles.get_page(page_number)

   return render(request, 'news/profile.html', {
        'articles_by_followed_authors': articles_by_followed_authors,
        'user': user,
        'page_obj':page_obj
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
            return HttpResponseRedirect(reverse("homepage"))
        else:
            return render(request, "news/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "news/login.html")
    
def follow_status(request, author_id):
    if request.user.is_authenticated:
        following = request.user
        author_followed = Author.objects.get(pk=author_id)
        existing_follower = Following.objects.filter(user_following=following, author_followed=author_followed).exists()
        return JsonResponse({"following": existing_follower})
    else:
        return JsonResponse({"following": False})
    
def search(request, search_article):
    search_articles = Article.objects.filter(Q(title__icontains=search_article) & Q(content__icontains=search_article))
    return render(request, "news/search.html",{
        "article":search_articles
    })

def follow(request, author_id):
    if request.method == "POST":
        following = request.user
        author_followed = Author.objects.get(pk=author_id)
        existing_follower = Following.objects.filter(user_following=following, author_followed=author_followed).first()
        if existing_follower:
            existing_follower.delete()
            return JsonResponse({"message":"unfollowed"})
        else:
            new_follow= Following(
                user_following=following,
                author_followed=author_followed
            )
            new_follow.save()
            return JsonResponse({"message":"followed"})
    elif json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON data"}, status=400)


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
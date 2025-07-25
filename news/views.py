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
from django.http import JsonResponse
from django.utils import timezone
from allauth.account.views import SignupView, LoginView

from newsapi import NewsApiClient

from .models import User, Section, Article, Author, Comment, Image, Following, Profile, Like
from cms.models import Homepage
# Create your views here.
             
def index(request):
    homepage = Homepage.objects.latest('date_created')

    featured_articles = homepage.featured_articles.all()
    featured_404 = homepage.featured_404.all()
    featured_electric = homepage.featured_electric.all()

    all_sections = Section.objects.all()

    return render(request, "news/homepage.html", {
        "homepage": homepage,
        "hero_article": homepage.hero_article,
        "featured_articles": featured_articles,
        "featured_404":featured_404,
        "featured_electric":featured_electric,
        "all_sections": all_sections
    })

def article_details(request, section_url_name, url):
    section = get_object_or_404(Section, section_url_name=section_url_name)
    article = get_object_or_404(Article, url=url, section=section)
    comments= Comment.objects.filter(article=article).order_by("-created_date")
    return render(request, "news/article.html", {
        "article": article,
        "section": section,
        "comments":comments
    })

def comment(request, article_id):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)

        if data.get("text") is not None:
            text = data["text"]
            this_commenter = request.user
            this_article = Article.objects.get(id=article_id)

            new_comment = Comment(
                comment_text=text,
                commenter=this_commenter,
                article=this_article,
                created_date=timezone.now()
            )
            new_comment.save()
            response_data = {
                "text": new_comment.comment_text,
                "commenter": str(new_comment.commenter),  
                "article": article_id,
            }
            return JsonResponse(response_data)
        else:
            return JsonResponse({"error": "Comment text missing"}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=405)

def like_status(request, comment_id):
    if request.user.is_authenticated:
        liker = request.user
        comment = get_object_or_404(Comment, pk=comment_id)
        existing_like = Like.objects.filter(comment_liked=comment, liker=liker).exists()
        return JsonResponse({"liked": existing_like})
    else:
        return JsonResponse({"liked": False})

def like(request, comment_id):
    if request.method == "POST":
        liker = request.user
        comment = get_object_or_404(Comment, pk=comment_id)
        existing_like = Like.objects.filter(comment_liked=comment, liker=liker).first()
        if existing_like:
            existing_like.delete()
            return JsonResponse({"message": "like removed"})
        else:
            new_like = Like(
                liker=liker,
                comment_liked=comment
            )
            new_like.save()
            return JsonResponse({"message": "like added"})
    elif json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON data"}, status=400)

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
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching news: {e}")
        return {}

def load_news(request):
    query = 'technology'  
    news_data = fetch_news(query)
    news_articles = news_data.get('articles', [])
    
    articles = Paginator(news_articles, 10)
    page_number = request.GET.get("page")
    page_obj = articles.get_page(page_number)

    return render(request, 'news/news.html', {
        'news_articles': news_articles, 
        'page_obj': page_obj  
    })

def profile(request, user_username):
   user = get_object_or_404(User, username=user_username)
   followed_authors = Following.objects.filter(user_following=user).values_list('author_followed', flat=True)
   articles_by_followed_authors = Article.objects.filter(byline__in=followed_authors)
   
   articles = Paginator(articles_by_followed_authors, 10)
   page_number = request.GET.get("page")
   page_obj = articles.get_page(page_number)

   return render(request, 'news/dashboard.html', {
        'articles_by_followed_authors': articles_by_followed_authors,
        'user': user,
        'page_obj':page_obj
    })

def follow_status(request, author_id):
    if request.user.is_authenticated:
        following = request.user
        author_followed = Author.objects.get(pk=author_id)
        existing_follower = Following.objects.filter(user_following=following, author_followed=author_followed).exists()
        return JsonResponse({"following": existing_follower})
    else:
        return JsonResponse({"following": False})

def get_query(request, query):
    search_article = request.GET.get('q')
    if search_article:
        return search(request, search_article)

def search(request, search_q):
    search_results = Article.objects.filter(Q(headline__icontains=search_q) | Q(content__icontains=search_q))
    articles = Paginator(search_results, 10)
    page_number = request.GET.get("page")
    page_obj = articles.get_page(page_number)
    return render(request, "news/search.html",{
        "search_results":search_results,
        "search_q":search_q,
        "page_obj":page_obj
    })

def about(request):
    return render(request, 'news/about.html')

def contact(request):
    return render(request, 'news/contact.html',{
        'EMAILJS_USER_ID': settings.EMAILJS_USER_ID,
        'EMAILJS_SERVICE_ID': settings.EMAILJS_SERVICE_ID,
        'EMAILJS_TEMPLATE_ID': settings.EMAILJS_TEMPLATE_ID,
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

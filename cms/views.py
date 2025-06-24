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
from news.models import Article, User, Image, Author, Section
from .models import Homepage
from .forms import ArticleForm, HomepageForm, AuthorForm, ImageForm, SectionForm
from django.db.models import Q
from django.core.paginator import Paginator
from haystack.query import SearchQuerySet
from simple_history.models import HistoricalRecords

# Create your views here.

#index
@login_required
def cms_dashboard(request):       
    # Get articles with author information and pagination
    articles_list = Article.objects.select_related('byline').order_by("-date")
    
    # Pagination
    paginator = Paginator(articles_list, 20)  # Show 20 articles per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'cms/dashboard.html', {
        'articles': page_obj,
        'page_obj': page_obj
    })

#article
@login_required
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

@login_required
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
@login_required
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

@login_required
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
@login_required
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

@login_required
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
@login_required
def get_image_url(request, image_id): 
    image = get_object_or_404(Image, id=image_id)
    url = image.get_image_url()
    print(url)
    return JsonResponse({'image_url': url})

#section
@login_required
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

@login_required
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
@login_required
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
@login_required
def get_query(request):
    search_q = request.GET.get('q', '')
    search_type = request.GET.get('type', '')

    if search_type == 'author':
        results = Author.objects.filter(Q(byline__icontains=search_q) | Q(author_bio__icontains=search_q))
    else:  # default to article
        results = Article.objects.filter(Q(headline__icontains=search_q) | Q(content__icontains=search_q))

    paginator = Paginator(results, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'cms/search.html', {
        'page_obj': page_obj,
        'search_q': search_q,
        'search_type': search_type,
    })

#delete
@login_required
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

@login_required
def create_user(request):
    # Only allow superusers to create users
    if not request.user.is_superuser:
        return HttpResponseRedirect(reverse("cms_dashboard"))
    
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        is_staff = request.POST.get("is_staff") == "on"
        is_superuser = request.POST.get("is_superuser") == "on"
        
        # Check if username already exists
        if User.objects.filter(username=username).exists():
            return render(request, "cms/create_user.html", {
                "message": "Username already taken.",
                "form_data": request.POST
            })
        
        # Check if email already exists
        if User.objects.filter(email=email).exists():
            return render(request, "cms/create_user.html", {
                "message": "Email already taken.",
                "form_data": request.POST
            })
        
        try:
            # Create the user
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                is_staff=is_staff,
                is_superuser=is_superuser
            )
            
            return render(request, "cms/create_user.html", {
                "success_message": f"User '{username}' created successfully!"
            })
            
        except Exception as e:
            return render(request, "cms/create_user.html", {
                "message": f"Error creating user: {str(e)}",
                "form_data": request.POST
            })
    
    return render(request, "cms/create_user.html")

@login_required
def list_users(request):
    # Only allow superusers to view user list
    if not request.user.is_superuser:
        return HttpResponseRedirect(reverse("cms_dashboard"))
    
    users = User.objects.all().order_by('username')
    return render(request, "cms/list_users.html", {
        'users': users
    })

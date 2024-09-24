from django.urls  import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from . import views


urlpatterns = [
    path('admin/clearcache/', include('clearcache.urls')),
    path("admin/", admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path("", views.index, name="homepage"),
    path('tinymce/', include('tinymce.urls')),
    path("section/<str:section_url_name>", views.section, name="section"),
    path("fetch-news/", views.fetch_news, name='fetch_news'),
    path("follow/<int:author_id>", views.follow, name="follow"),
    path("follow_status/<int:author_id>", views.follow_status, name="follow_status"),
    path("articles/<str:section_url_name>/<str:url>", views.article_details, name="article_details"),
    path("comment/<int:article_id>",views.comment, name="comment"),
    path("like/<int:comment_id>", views.like, name="like"),
    path("like_status/<int:comment_id>", views.like_status, name="like_status"),
    path("contributors/<str:author_slug>", views.author_page, name="author_page"),
    path("profile/<str:user_username>", views.profile, name="profile"),
    path("get_query", views.get_query, name="get_query"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
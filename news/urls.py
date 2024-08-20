from django.urls  import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from . import views


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.index, name="homepage"),
    path('tinymce/', include('tinymce.urls')),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("section/<str:section_url_name>", views.section, name="section"),
    path("fetch-news/", views.fetch_news, name='fetch_news'),
    path("follow/<int:author_id>", views.follow, name="follow"),
    path("follow_status/<int:author_id>", views.follow_status, name="follow_status"),
    path("articles/<str:section_url_name>/<str:url>", views.article_details, name="article_details"),
    path("contributors/<str:author_slug>", views.author_page, name="author_page")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
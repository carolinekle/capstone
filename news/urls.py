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
    path("sections/<str:section_url_name>", views.section, name="section"),
    path("fetch-news/", views.fetch_news, name='fetch_news'),
    path("section/<str:section_url_name>/<str:url>", views.article_details, name="article_details"),
    path("contributors/<str:author_slug>", views.author_page, name="author_page")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
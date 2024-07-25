from django.urls  import path
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [
    path("", views.index, name="homepage"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("404", views.page_not_found, name="404"),
    path("electrc-drama", views.electric_drama, name="electric-drama"),
    path("news", views.load_news, name="news"),
    path('fetch-news/', views.fetch_news, name='fetch_news')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
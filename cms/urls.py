from django.urls  import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [
    path('tinymce/', include('tinymce.urls')),
    path('', views.cms_dashboard, name='cms_dashboard'),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('create/', views.create_article, name='create_article'),
    path('edit/<int:article_id>/', views.edit_article, name='edit_article'),
    path('delete/<int:article_id>/', views.delete_article, name='delete_article'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
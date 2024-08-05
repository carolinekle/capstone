from django.urls  import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [
    path('tinymce/', include('tinymce.urls')),
    path('', views.cms_dashboard, name='cms_dashboard'),
    path('create/', views.cms_create_article, name='cms_create_article'),
    path('edit/<int:article_id>/', views.cms_edit_article, name='cms_edit_article'),
    path('delete/<int:article_id>/', views.cms_delete_article, name='cms_delete_article'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
from django.urls  import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from . import views


urlpatterns = [
    path('admin/clearcache/', include('clearcache.urls')),
    path("admin/", admin.site.urls),
    path('tinymce/', include('tinymce.urls')),
    path('', views.cms_dashboard, name='cms_dashboard'),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("delete_article/<int:article_id>", views.delete_article, name="delete_article"),
    path("edit", views.edit_homepage, name="edit_homepage"),
    path('create/', views.create_article, name='create_article'),
    path('edit/<int:article_id>/', views.edit_article, name='edit_article'),
    path('delete/<int:article_id>/', views.delete_article, name='delete_article'),
    path('create_author', views.create_author, name="create_author"),
    path('create_section', views.create_section, name="create_section"),
    path('edit_section/<int:section_id>', views.edit_section, name="edit_section"),
    path('create_image/', views.create_image, name="create_image"),
    path('create_like', views.create_like, name="create_like")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
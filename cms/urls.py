from django.urls  import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from . import views


urlpatterns = [
    path('admin/clearcache/', include('clearcache.urls')),
    path('search/', include('haystack.urls')),
    path("admin/", admin.site.urls),
    path('tinymce/', include('tinymce.urls')),
    path('', views.cms_dashboard, name='cms_dashboard'),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    # edit
    path("edit/homepage/", views.edit_homepage, name="edit_homepage"),
    path('edit/section/<int:section_id>/', views.edit_section, name="edit_section"),
    path('edit/article/<int:article_id>/', views.edit_article, name='edit_article'),
    path('edit/author/<int:author_id>/', views.edit_author, name="edit_author"),
    path('edit/image/<int:image_id>', views.edit_image, name="edit_image"),
    #create
    path('create_article/', views.create_article, name='create_article'),
    path('create_author', views.create_author, name="create_author"),
    path('create_section', views.create_section, name="create_section"),
    path('create_image/', views.create_image, name="create_image"),
    #manage
    path('get_image_url/<int:image_id>/', views.get_image_url, name='get_image_url'),
    path("delete_article/<int:article_id>", views.delete_article, name="delete_article"),
    path("get_query", views.get_query, name="get_query"),
    path('delete/<int:article_id>/', views.delete_article, name='delete_article'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
"""
URL configuration for socialnet project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from core.views import *
from django.conf import settings # !
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', homepage),
    path('posts/<int:id>/', post_detail, name='post-detail'),
    path('profile/<int:id>/', profile_detail, name='profile'),
    path('shorts/', shorts, name='shorts-list'),
    path('short/<int:id>/', short_info, name='shorts-info'),
    path('saved_posts/', saved_posts_list, name='saved-posts'),
    path('<int:user_id>/', user_posts, name='user-posts'),
    path('add-post/', create_post, name='add-post'),
    path('add-short/', add_short, name='add-short'),
    path('add-saved/', add_saved, name='add-saved'),
    path('search/', search, name='search'),
    path('search-result/', search_result, name='search-result'),
    path('users/', include('userapp.urls')),

]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

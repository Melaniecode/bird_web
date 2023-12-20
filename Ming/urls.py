"""Ming URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path
from order import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    ### function
    path('getMyloc/',views.getMyloc),

    ### homepage
    path('',views.index),

    ### openAI
    path('openAI_gpt/',views.openAI_gpt),

    ### about
    path('about/', views.about),

    ### birdlist
    path('birdlist/', views.birdlist),

    ### guide
    path('guide/', views.guide),

    ### realtime
    path('realtime/', views.realtime),

    #### database
    path('upload_img/', views.upload_img),

    #### test
    path('index_test/', views.index_test),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

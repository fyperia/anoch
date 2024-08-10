"""
URL configuration for anochSite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import include, path

urlpatterns = [
    path('db/', include('rules_db.urls')),
    path('admin/', admin.site.urls),
    path('prose/', include('prose.urls')),
]

admin.site.site_header = 'Knight Realms - Anoch DB'
admin.site.site_title = 'KR Anoch Admin Panel'
admin.site.index_title = 'Admin Index'

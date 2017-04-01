"""HealthNet URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
# authtest/urls.py
from django.conf.urls import include, url
from django.contrib import admin
# Add this import
from django.contrib.auth import views
from users.forms import LoginForm
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
                  url(r'^admin/', include(admin.site.urls)),
                  url(r'', include('cal.urls')),  # not sure where we want the calendar urls yet
                  url(r'', include('users.urls')),  # All urls from users are at the base
                  url(r'^login/$', views.login, {'template_name': 'users/login.html', 'authentication_form': LoginForm},
                      name='login'),
                  url(r'^accounts/login/$', views.login,
                      {'template_name': 'users/login.html', 'authentication_form': LoginForm}, name='login'),
                  url(r'^logout/$', views.logout, {'next_page': '/login'}),

              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL,
                                                                                           document_root=settings.MEDIA_ROOT)

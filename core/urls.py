"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from rest_framework_swagger.views import get_swagger_view
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView
)

import user.urls as user_urls
from user.api import viewsets as user_api_views
from core.api import viewsets as report_api_views

schema_view = get_swagger_view(title='Alliance Swagger')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('authentication/login/', user_api_views.AuthenticationJWTView.as_view(), name='authentication_login'),
    path('authentication/profile/', user_api_views.UserProfileView.as_view(), name='authentication_profile'),
    path('authentication/verify/', TokenVerifyView.as_view(), name='authentication_token_verify'),
    path('authentication/refresh/', TokenRefreshView.as_view(), name='authentication_token_refresh'),
    path('authentication/register/', user_api_views.api_authentication_register, name='authentication_register'),
    path('authorization/', include(user_urls), name='authorization'),
    path('reports/ar/', report_api_views.api_report_aging_report, name='report_ar'),
    path('reports/ar/location/', report_api_views.api_report_by_location, name='report_ar_location'),
    path('reports/ar/payer-group/', report_api_views.api_report_aging_payer_group, name='report_ar_payer_group'),
    path('reports/ar/balance/', report_api_views.api_report_balance, name='report_balance'),
    path('reports/ar/count/', report_api_views.api_report_count, name='report_count'),
    path('reports/ar/profiles/', report_api_views.api_report_profiles, name='report_profiles'),
    path('swagger/', schema_view, name='swagger ui'),
]

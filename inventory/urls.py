from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('products.urls')),
    path('swagger/', include('products.swagger')),
    path('api-token-auth/', views.obtain_auth_token)
]

from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('store_message.urls', namespace='store_message')),
    path('users/', include('users.urls', namespace='users')),
]

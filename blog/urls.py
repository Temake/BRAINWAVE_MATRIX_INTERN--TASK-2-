
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('a/', admin.site.urls),
    path('', include('blogger.urls')),
    path("__reload__/", include("django_browser_reload.urls")),
]
# In your main urls.py
handler404 = 'blogger.views.custom_404_view'
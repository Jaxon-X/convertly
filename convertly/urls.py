
from django.contrib import admin
from django.urls import path

from convertly.views import main_page

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', main_page, name='main_page'),
]

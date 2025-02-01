from convertly.views import FileConvertView
from django.urls import path

urlpatterns = [
    path('doc-to-pdf/', FileConvertView.as_view(), name='file_convertor'),
]
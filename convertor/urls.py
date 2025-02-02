from convertor.views import FileConvertView, FileDownloadView
from django.urls import path

urlpatterns = [
    path('doc-to-pdf/', FileConvertView.as_view(), name='file_convertor'),
    path("download/<str:filename>/", FileDownloadView.as_view(), name='file-download')
]
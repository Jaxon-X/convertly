from convertor.views import DocToPdfView, FileDownloadView, DocToTxtView, ExcelToPdfView, CsvToExcelView, \
    ImageToPdfView, OdtToPdfView, CheckStatusConvertView
from django.urls import path

urlpatterns = [
    path('doc-to-pdf/', DocToPdfView.as_view(), name='doc-to-pdf'),
    path("download/<str:filename>/", FileDownloadView.as_view(), name='file-download'),
    path("doc-to-txt/", DocToTxtView.as_view(), name="doc-to-txt"),
    path("excel-to-pdf/", ExcelToPdfView.as_view(), name="excel-to-pdf"),
    path("csv-to-excel/", CsvToExcelView.as_view(), name="csv-to-excel"),
    path("image-to-pdf/", ImageToPdfView.as_view(), name="image-to-pdf"),
    path("odt-to-pdf/", OdtToPdfView.as_view(), name="odt-to-pdf"),
    path('status/<str:task_id>/', CheckStatusConvertView.as_view(), name='check-status')
]
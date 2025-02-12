import os
from django.core import cache
from django.http import FileResponse
from convertor.services.doctopdf import convert_doc_to_pdf
from convertor.services.exceltopdf import convert_excel_to_pdf
from convertor.services.imagetopdf import convert_image_to_pdf
from convertor.services.doctotxt import convert_doc_to_txt
from convertor.services.csvtoexcel import convert_csv_to_excel
from convertor.services.odttopdf import convert_odt_to_pdf
from django.core.files.storage import default_storage

from celery import shared_task
import shutil

@shared_task(bind=True, max_retries = 3)
def convertor_doc_to_pdf(self, input_file):
    return convert_doc_to_pdf(input_file)

@shared_task(bind=True, max_retries = 3)
def convertor_excel_to_pdf(input_file):
    return convert_excel_to_pdf(input_file)

@shared_task(bind=True, max_retries = 3)
def convertor_image_to_pdf(input_file):
    return convert_image_to_pdf(input_file)


@shared_task(bind=True, max_retries = 3)
def convertor_doc_to_txt(input_file):
    return convert_doc_to_txt(input_file)

@shared_task(bind=True, max_retries = 3)
def convertor_csv_to_excel(input_file):
    return convert_csv_to_excel(input_file)

@shared_task(bind=True, max_retries = 3)
def convertor_odt_to_pdf(input_file):
    return convert_odt_to_pdf(input_file)

#
# @shared_task
# def cleanup_files():
#     converted_files_path = "/home/jaxon/Python_Projects/convertly/converted_files"
#     upload_files_path = "/home/jaxon/Python_Projects/convertly/upload_files"
#     if os.path.exists(converted_files_path):
#         shutil.rmtree(converted_files_path)
#     elif os.path.exists(upload_files_path):
#         shutil.rmtree(upload_files_path)


@shared_task
def download_converted_file(filename):
    response = FileResponse(open(file_path, 'rb'))
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    last_upload_file = cache.get('last_upload_file')
    default_storage.delete(last_upload_file)
    cache.delete('last_upload_file')
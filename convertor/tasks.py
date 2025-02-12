from convertor.services.doctopdf import convert_doc_to_pdf
from convertor.services.exceltopdf import convert_excel_to_pdf
from convertor.services.imagetopdf import convert_image_to_pdf
from convertor.services.doctotxt import convert_doc_to_txt
from convertor.services.csvtoexcel import convert_csv_to_excel
from convertor.services.odttopdf import convert_odt_to_pdf
from django.core.files.storage import default_storage

from celery import shared_task

@shared_task(bind=True, max_retries = 3)
def convertor_doc_to_pdf(input_file):
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


@shared_task
def cleanup_files():
    default_storage.delete("/home/jaxon/Python_Projects/convertly/converted_files")
    default_storage.delete("/home/jaxon/Python_Projects/convertly/upload_files")
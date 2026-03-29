from pathlib import Path

from convertor.services.doctopdf import convert_doc_to_pdf
from convertor.services.exceltopdf import convert_excel_to_pdf
from convertor.services.imagetopdf import convert_image_to_pdf
from convertor.services.doctotxt import convert_doc_to_txt
from convertor.services.csvtoexcel import convert_csv_to_excel
from convertor.services.odttopdf import convert_odt_to_pdf

from celery import shared_task

UPLOADED_FILE_TTL_SECONDS = 10 * 60
CONVERTED_FILE_TTL_SECONDS = 15 * 60


def _schedule_file_cleanup(file_path, countdown):
    if file_path:
        delete_file.apply_async(args=[file_path], countdown=countdown)


def _finalize_converted_file(converted_file):
    if not converted_file or not Path(converted_file).exists():
        raise ValueError("Conversion failed or the converted file was not created.")

    _schedule_file_cleanup(converted_file, CONVERTED_FILE_TTL_SECONDS)
    return converted_file

@shared_task(bind=True, max_retries = 3)
def convertor_doc_to_pdf(self, input_file):
    return _finalize_converted_file(convert_doc_to_pdf(input_file))

@shared_task(bind=True, max_retries = 3)
def convertor_excel_to_pdf(self,input_file):
    return _finalize_converted_file(convert_excel_to_pdf(input_file))

@shared_task(bind=True, max_retries = 3)
def convertor_image_to_pdf(self,input_file):
    return _finalize_converted_file(convert_image_to_pdf(input_file))


@shared_task(bind=True, max_retries = 3)
def convertor_doc_to_txt(self,input_file):
    return _finalize_converted_file(convert_doc_to_txt(input_file))

@shared_task(bind=True, max_retries = 3)
def convertor_csv_to_excel(self,input_file):
    return _finalize_converted_file(convert_csv_to_excel(input_file))

@shared_task(bind=True, max_retries = 3)
def convertor_odt_to_pdf(self,input_file):
    return _finalize_converted_file(convert_odt_to_pdf(input_file))


@shared_task
def delete_file(file_path):
    path = Path(file_path)
    if path.exists() and path.is_file():
        path.unlink()



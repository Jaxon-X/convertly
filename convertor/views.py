from celery.result import AsyncResult
from django.core import signing
from django.core.signing import BadSignature, SignatureExpired
from django.http import FileResponse
import os
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import  APIView

from convertor.paths import CONVERTED_FILES_DIR, INPUT_FILES_DIR
from convertor.serializers import FileUploadSerializer
from .tasks import (
    CONVERTED_FILE_TTL_SECONDS,
    UPLOADED_FILE_TTL_SECONDS,
    convertor_csv_to_excel,
    convertor_doc_to_pdf,
    convertor_doc_to_txt,
    convertor_excel_to_pdf,
    convertor_image_to_pdf,
    convertor_odt_to_pdf,
    delete_file,
)

DOWNLOAD_TOKEN_SALT = "convertor.download"


def save_uploaded_file(uploaded_file):
    input_file_path = os.path.join(INPUT_FILES_DIR, uploaded_file.name)
    os.makedirs(INPUT_FILES_DIR, exist_ok=True)

    with open(input_file_path, 'wb') as f:
        for chunk in uploaded_file.chunks():
            f.write(chunk)

    if os.path.exists(input_file_path):
        delete_file.apply_async(args=[input_file_path], countdown=UPLOADED_FILE_TTL_SECONDS)
        return input_file_path

    return None


def build_download_token(filename):
    return signing.dumps({"filename": filename}, salt=DOWNLOAD_TOKEN_SALT)


def validate_download_token(token, filename):
    payload = signing.loads(
        token,
        salt=DOWNLOAD_TOKEN_SALT,
        max_age=CONVERTED_FILE_TTL_SECONDS,
    )
    return payload.get("filename") == filename


def build_conversion_response(task, filename, input_file_path):
    return Response(
        {
            "message": "File was successfully converted",
            "input_file_path": input_file_path,
            "filename": filename,
            "task_id": task.id,
            "download_token": build_download_token(filename),
        },
        status=status.HTTP_200_OK,
    )

class DocToPdfView(APIView):    
    parser_classes = [MultiPartParser, FormParser]
    def post(self, request):
        try:
            file = request.FILES['file']
            file_name = file.name
            input_filename, extension= os.path.splitext(file_name)

            serializer = FileUploadSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


            converted_filename = input_filename + ".pdf"
            input_file_path = save_uploaded_file(file)
            if not input_file_path:
                return Response({"msg": "File didn't write in file"})

            converted = convertor_doc_to_pdf.delay(input_file_path)

            return build_conversion_response(converted, converted_filename, input_file_path)

        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )



class  DocToTxtView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    def post(self, request):
        try:

            file = request.FILES['file']
            file_name = file.name
            input_filename, extension= os.path.splitext(file_name)

            serializer = FileUploadSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            converted_filename = input_filename + ".txt"
            input_file_path = save_uploaded_file(file)
            if not input_file_path:
                return Response({"msg": "File didn't write to file"})

            converted = convertor_doc_to_txt.delay(input_file_path)

            return build_conversion_response(converted, converted_filename, input_file_path)

        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ExcelToPdfView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    def post(self, request):
        try:

            file = request.FILES['file']
            file_name = file.name
            input_filename, extension= os.path.splitext(file_name)
            serializer = FileUploadSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            converted_filename = input_filename + ".pdf"
            input_file_path = save_uploaded_file(file)
            if not input_file_path:
                return Response({"msg": "File didn't write to file"})

            converted = convertor_excel_to_pdf.delay(input_file_path)

            return build_conversion_response(converted, converted_filename, input_file_path)

        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class CsvToExcelView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    def post(self, request):
        try:

            file = request.FILES['file']
            file_name = file.name
            input_filename, extension= os.path.splitext(file_name)
            serializer = FileUploadSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            converted_filename = input_filename + ".xlsx"
            input_file_path = save_uploaded_file(file)
            if not input_file_path:
                return Response({"msg": "File didn't write to file"})

            converted = convertor_csv_to_excel.delay(input_file_path)
            return build_conversion_response(converted, converted_filename, input_file_path)

        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class ImageToPdfView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    def post(self, request):
        try:

            file = request.FILES['file']
            file_name = file.name
            input_filename, extension= os.path.splitext(file_name)
            serializer = FileUploadSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            converted_filename = input_filename + ".pdf"
            input_file_path = save_uploaded_file(file)
            if not input_file_path:
                return Response({"msg": "File didn't write to file"})

            converted = convertor_image_to_pdf.delay(input_file_path)
            return build_conversion_response(converted, converted_filename, input_file_path)

        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class OdtToPdfView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        try:

            file = request.FILES['file']
            file_name = file.name
            input_filename, extension= os.path.splitext(file_name)

            serializer = FileUploadSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            converted_filename = input_filename + ".pdf"
            input_file_path = save_uploaded_file(file)
            if not input_file_path:
                return Response({"msg": "File didn't write to file"})

            converted = convertor_odt_to_pdf.delay(input_file_path)

            return build_conversion_response(converted, converted_filename, input_file_path)

        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )



class FileDownloadView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, filename):
        try:
            token = request.query_params.get("token")
            if not token:
                return Response({"error": "Download token is required"}, status=status.HTTP_400_BAD_REQUEST)

            try:
                if not validate_download_token(token, filename):
                    return Response({"error": "Download token is invalid"}, status=status.HTTP_403_FORBIDDEN)
            except SignatureExpired:
                return Response({"error": "Download token has expired"}, status=status.HTTP_403_FORBIDDEN)
            except BadSignature:
                return Response({"error": "Download token is invalid"}, status=status.HTTP_403_FORBIDDEN)

            converted_file = os.path.join(CONVERTED_FILES_DIR, filename)
            if not os.path.exists(converted_file):
                return Response({"error": "File not found"}, status=status.HTTP_400_BAD_REQUEST)

            response = FileResponse(open(converted_file, 'rb'))
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            return response

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CheckStatusConvertView(APIView):
    def get(self, request, task_id):
        try:
            task_result = AsyncResult(task_id)
            return Response(
                {
                    'task_status':task_result.status,
                    'ready': task_result.ready()
                }
            )
        except Exception as e:
            return Response(
                {'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


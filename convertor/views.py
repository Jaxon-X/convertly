from django.conf import settings
from rest_framework.views import  APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.core.cache import cache

from celery.result import AsyncResult

from convertor.serializers import FileUploadSerializer
from rest_framework import status
from django.core.files.storage import default_storage
from django.http import FileResponse
import os

from .tasks import convertor_csv_to_excel, convertor_doc_to_pdf, convertor_excel_to_pdf, convertor_odt_to_pdf, convertor_image_to_pdf, convertor_doc_to_txt

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
            input_file_path = f"/tmp/input_files/{file_name}"
            os.makedirs("/tmp/input_files", exist_ok=True)

            with open(input_file_path, 'wb') as f:
                for chunk in file.chunks():
                    f.write(chunk)
            if os.path.exists(input_file_path):
                print("File written in disk")

            converted_file_path = f"/tmp/converted_files/{converted_filename}"
            cache.set("last_upload_file_path", converted_file_path, timeout=300)
            converted = convertor_doc_to_pdf.delay(input_file_path)

            return  Response({
                "message": "File was successfully converted",
                "input_file_path": input_file_path,
                "converted_file_path": converted_file_path,
                "task_id": converted.id
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )



class  DocToTxtView(APIView):

    def post(self, request):
        try:

            file = request.FILES['file']
            file_name = file.name
            filename, extension= os.path.splitext(file_name)
            serializer = FileUploadSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


            filename2 = filename + ".txt"
            file_path = default_storage.save(f'upload_files/{file.name}', file)
            input_file = os.path.join(settings.MEDIA_ROOT, file_path)
            cache.set("last_upload_file", input_file, timeout=300)
            converted = convertor_doc_to_txt.delay(input_file)

            return  Response({
                "message": "File was successfully converted",
                "input_file_path": input_file,
                "filename": filename2,
                "task_id": converted.id
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ExcelToPdfView(APIView):

    def post(self, request):
        try:

            file = request.FILES['file']
            file_name = file.name
            filename, extension= os.path.splitext(file_name)
            serializer = FileUploadSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


            filename2 = filename + ".pdf"
            file_path = default_storage.save(f'upload_files/{file.name}', file)
            input_file = os.path.join(settings.MEDIA_ROOT, file_path)
            cache.set("last_upload_file", input_file, timeout=300)
            converted = convertor_excel_to_pdf.delay(input_file)

            return  Response({
                "message": "File was successfully converted",
                "input_file_path": input_file,
                "filename": filename2,
                "task_id": converted.id
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class CsvToExcelView(APIView):

    def post(self, request):
        try:

            file = request.FILES['file']
            file_name = file.name
            filename, extension= os.path.splitext(file_name)
            serializer = FileUploadSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


            filename2 = filename + ".xlsx"
            file_path = default_storage.save(f'upload_files/{file.name}', file)
            input_file = os.path.join(settings.MEDIA_ROOT, file_path)
            cache.set("last_upload_file", input_file, timeout=300)
            converted = convertor_csv_to_excel.delay(input_file)
            return  Response({
                "message": "File was successfully converted",
                "input_file_path": input_file,
                "filename": filename2,
                "task_id": converted.id
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class ImageToPdfView(APIView):

    def post(self, request):
        try:

            file = request.FILES['file']
            file_name = file.name
            filename, extension= os.path.splitext(file_name)
            serializer = FileUploadSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


            filename2 = filename + ".pdf"
            file_path = default_storage.save(f'upload_files/{file.name}', file)
            input_file = os.path.join(settings.MEDIA_ROOT, file_path)
            cache.set("last_upload_file", input_file, timeout=300)
            converted = convertor_image_to_pdf.delay(input_file)
            return  Response({
                "message": "File was successfully converted",
                "input_file_path": input_file,
                "filename": filename2,
                "task_id": converted.id
            }, status=status.HTTP_200_OK)

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
            filename, extension= os.path.splitext(file_name)

            serializer = FileUploadSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


            filename2 = filename + ".pdf"
            file_path = default_storage.save(f'upload_files/{file.name}', file)
            input_file = os.path.join(settings.MEDIA_ROOT, file_path)
            cache.set("last_upload_file", input_file, timeout=300)
            converted = convertor_odt_to_pdf.delay(input_file)

            return  Response({
                "message": "File was successfully converted",
                "input_file_path": input_file,
                "filename": filename2,
                "task_id": converted.id
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )



class FileDownloadView(APIView):

    def get(self, request, filename):
        try:
            last_upload_file = cache.get('last_upload_file_path')
            print(last_upload_file)
            converted_file = f"/tmp/converted_files/{filename}"
            if not os.path.exists(converted_file):
                return Response({"error": "File not found"}, status=status.HTTP_400_BAD_REQUEST)

            response = FileResponse(open(converted_file, 'rb'))
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            os.remove(last_upload_file)
            cache.delete('last_upload_file')
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


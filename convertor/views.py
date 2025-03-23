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
            if not os.path.exists(input_file_path):
                return Response({"msg": "File didn't write in file"})

            cache.set("input_file_path", input_file_path, timeout=300)
            converted = convertor_doc_to_pdf.delay(input_file_path)

            return  Response({
                "message": "File was successfully converted",
                "input_file_path": input_file_path,
                "filename": converted_filename,
                "task_id": converted.id
            }, status=status.HTTP_200_OK)

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
            input_file_path = f"/tmp/input_files/{file_name}"
            os.makedirs("/tmp/input_files", exist_ok=True)

            with open(input_file_path, 'wb') as f:
                for chunk in file.chunks():
                    f.write(chunk)
            if not os.path.exists(input_file_path):
                return Response({"msg": "File didn't write to file"})

            cache.set("input_file_path", input_file_path, timeout=300)
            converted = convertor_doc_to_txt.delay(input_file_path)

            return  Response({
                "message": "File was successfully converted",
                "input_file_path": input_file_path,
                "filename": converted_filename,
                "task_id": converted.id
            }, status=status.HTTP_200_OK)

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
            input_file_path = f"/tmp/input_files/{file_name}"
            os.makedirs("/tmp/input_files", exist_ok=True)

            with open(input_file_path, 'wb') as f:
                for chunk in file.chunks():
                    f.write(chunk)
            if not os.path.exists(input_file_path):
                return Response({"msg": "File didn't write to file"})

            cache.set("input_file_path", input_file_path, timeout=300)
            converted = convertor_excel_to_pdf.delay(input_file_path)

            return  Response({
                "message": "File was successfully converted",
                "input_file_path": input_filename,
                "filename": converted_filename,
                "task_id": converted.id
            }, status=status.HTTP_200_OK)

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
            input_file_path = f"/tmp/input_files/{file_name}"
            os.makedirs("/tmp/input_files", exist_ok=True)

            with open(input_file_path, 'wb') as f:
                for chunk in file.chunks():
                    f.write(chunk)
            if not os.path.exists(input_file_path):
                return Response({"msg": "File didn't write to file"})

            cache.set("input_file_path", input_file_path, timeout=300)
            converted = convertor_csv_to_excel.delay(input_file_path)
            return  Response({
                "message": "File was successfully converted",
                "input_file_path": input_filename,
                "filename": converted_filename,
                "task_id": converted.id
            }, status=status.HTTP_200_OK)

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
            input_file_path = f"/tmp/input_files/{file_name}"
            os.makedirs("/tmp/input_files", exist_ok=True)

            with open(input_file_path, 'wb') as f:
                for chunk in file.chunks():
                    f.write(chunk)
            if not os.path.exists(input_file_path):
                return Response({"msg": "File didn't write to file"})

            cache.set("input_file_path", input_file_path, timeout=300)
            converted = convertor_image_to_pdf.delay(input_file_path)
            return  Response({
                "message": "File was successfully converted",
                "input_file_path": input_filename,
                "filename": converted_filename,
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
            if not os.path.exists(input_file_path):
                return Response({"msg": "File didn't write to file"})

            cache.set("input_file_path", input_file_path, timeout=300)
            converted = convertor_odt_to_pdf.delay(input_file_path)

            return  Response({
                "message": "File was successfully converted",
                "input_file_path": input_filename,
                "filename": converted_filename,
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
            input_file_path = cache.get('input_file_path')
            print(input_file_path)
            converted_file = f"/tmp/converted_files/{filename}"
            print(converted_file)
            if not os.path.exists(converted_file):
                return Response({"error": "File not found"}, status=status.HTTP_400_BAD_REQUEST)

            response = FileResponse(open(converted_file, 'rb'))
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            os.remove(converted_file)
            os.remove(input_file_path)
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


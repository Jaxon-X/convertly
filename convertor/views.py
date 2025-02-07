from django.conf import settings
from rest_framework.views import  APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.core.cache import cache
from convertly.settings import BASE_DIR

from convertor.serializers import FileUploadSerializer
from rest_framework import status
from django.core.files.storage import default_storage
from django.http import FileResponse
import os

from convertor.services.doctotxt import convert_doc_to_txt
from convertor.services.exceltopdf import convert_excel_to_pdf
from convertor.services.csvtoexcel import convert_csv_to_excel
from convertor.services.doctopdf import convert_doc_to_pdf
from convertor.services.imagetopdf import convert_image_to_pdf


class DocToPdfView(APIView):
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
            converted = convert_doc_to_pdf(input_file)

            return  Response({
                "message": "File was successfully converted",
                "input_file_path": input_file,
                "converted_file":converted,
                "filename": filename2
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
            converted = convert_doc_to_txt(input_file)

            return  Response({
                "message": "File was successfully converted",
                "input_file_path": input_file,
                "converted_file":converted,
                "filename": filename2
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
            converted = convert_excel_to_pdf(input_file)

            return  Response({
                "message": "File was successfully converted",
                "input_file_path": input_file,
                "converted_file":converted,
                "filename": filename2
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
            converted = convert_csv_to_excel(input_file)
            return  Response({
                "message": "File was successfully converted",
                "input_file_path": input_file,
                "converted_file":converted,
                "filename": filename2
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
            converted = convert_image_to_pdf(input_file)
            return  Response({
                "message": "File was successfully converted",
                "input_file_path": input_file,
                "converted_file":converted,
                "filename": filename2
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )



class FileDownloadView(APIView):
    def get(self, request, filename):
        file_path = os.path.join(BASE_DIR, 'converted_files', filename)
        if not os.path.exists(file_path):
            return Response({"error": "File not found"}, status=status.HTTP_400_BAD_REQUEST)

        response = FileResponse(open(file_path, 'rb'))
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        last_upload_file = cache.get('last_upload_file')
        default_storage.delete(last_upload_file)
        cache.delete('last_upload_file')
        return response
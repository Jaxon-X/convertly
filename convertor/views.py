from django.conf import settings
from rest_framework.views import  APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser

from convertly.settings import BASE_DIR
from convertor.services.doctopdf import convert_doc_to_pdf
from convertor.serializers import FileUploadSerializer
from rest_framework import status
from django.core.files.storage import default_storage
from django.http import FileResponse
import os


class FileConvertView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        try:

            file = request.FILES['file']
            file_name = file.name
            filename, extension= os.path.splitext(file_name)
            if (extension.lower() == ".doc" or extension.lower() == ".docx") == False:
                return Response({"error": "For only doc or docx file"}, status=status.HTTP_400_BAD_REQUEST)

            serializer = FileUploadSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


            filename2 = filename + ".pdf"
            file_path = default_storage.save(f'upload_files/{file.name}', file)
            input_file = os.path.join(settings.MEDIA_ROOT, file_path)
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


class FileDownloadView(APIView):
    def get(self, request, filename):
        file_path = os.path.join(BASE_DIR, 'converted_files', filename)
        if not os.path.exists(file_path):
            return Response({"error": "Filee not found"}, status=status.HTTP_400_BAD_REQUEST)

        response = FileResponse(open(file_path, 'rb'))
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response
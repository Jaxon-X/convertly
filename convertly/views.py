from django.conf import settings
from rest_framework.views import  APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from convertor.services.doctopdf import convert_doc_to_pdf
from convertor.serializers import FileUploadSerializer
from rest_framework import status
from django.core.files.storage import default_storage
import os

class FileConvertView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        try:
            serializer = FileUploadSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            file = request.FILES['file']
            print(file)

            file_path = default_storage.save(f'upload_files/{file.name}', file)
            full_file_path = os.path.join(settings.MEDIA_ROOT, file_path)
            convert_doc_to_pdf(full_file_path)

            return  Response({
                "message": "File was successfully converted",
                "file_path": full_file_path,
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )





from rest_framework import serializers

class FileUploadSerializer(serializers.Serializer):
    file = serializers.FileField()

    def validate(self, attrs):
        file = attrs.get('file')
        if not file.name.endswith('.docx'):
            raise serializers.ValidationError("Only .docx files are allowed.")
        return attrs




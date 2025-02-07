

from rest_framework import serializers

class FileUploadSerializer(serializers.Serializer):
    file = serializers.FileField()

    def validate(self, attrs):
        file = attrs.get('file')
        if file.name.endswith('.docx'):
            return self.validate_doc_file(attrs)
        elif file.name.endswith('.pdf'):
            return self.validate_pdf_file(attrs)
        elif file.name.endswith(".xls") or file.name.endswith(".xlsx"):
            return self.validate_excel_file(attrs)
        elif file.name.endswith('.csv'):
            return self.validate_csv_file(attrs)

    def validate_doc_file(self, attrs):
        file = attrs.get('file')
        if not file.name.endswith('.docx'):
            raise serializers.ValidationError("Only .docx files are allowed.")
        return attrs

    def validate_pdf_file(self, attrs):
        file = attrs.get('file')
        if not file.name.endswith('.pdf'):
            raise serializers.ValidationError("Only .pdf files are allowed.")
        return attrs

    def validate_excel_file(self, attrs):
        file = attrs.get('file')
        if (file.name.endswith('.xls') or file.name.endswith(".xlsx")) == False:
            raise serializers.ValidationError("Only .xlsx  files are allowed.")
        return attrs

    def validate_csv_file(self, attrs):
        file = attrs.get('file')
        if not (file.name.endswith('.csv')):
            raise serializers.ValidationError("Only .csv  files are allowed.")
        return attrs





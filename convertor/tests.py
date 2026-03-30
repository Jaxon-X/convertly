import os
import tempfile
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import SimpleTestCase, TestCase
from rest_framework.test import APIRequestFactory, force_authenticate

from convertor.paths import CONVERTED_FILES_DIR, INPUT_FILES_DIR
from convertor.tasks import (
    CONVERTED_FILE_TTL_SECONDS,
    UPLOADED_FILE_TTL_SECONDS,
    convertor_doc_to_pdf,
)
from convertor.views import (
    FileDownloadView,
    build_download_token,
    save_uploaded_file,
    validate_download_token,
)


class UploadLifecycleTests(SimpleTestCase):
    def test_save_uploaded_file_schedules_uploaded_file_cleanup_for_ten_minutes(self):
        uploaded_file = SimpleUploadedFile("example.docx", b"demo-content")

        with patch("convertor.views.delete_file.apply_async") as mocked_apply_async:
            file_path = save_uploaded_file(uploaded_file)

        self.assertTrue(os.path.exists(file_path))
        self.assertEqual(file_path, os.path.join(INPUT_FILES_DIR, "example.docx"))
        mocked_apply_async.assert_called_once_with(
            args=[file_path],
            countdown=UPLOADED_FILE_TTL_SECONDS,
        )
        os.remove(file_path)


class ConvertedLifecycleTests(SimpleTestCase):
    def test_conversion_task_schedules_converted_file_cleanup_for_fifteen_minutes(self):
        converted_path = os.path.join(CONVERTED_FILES_DIR, "example.pdf")

        with patch("convertor.tasks.convert_doc_to_pdf", return_value=converted_path), patch(
            "convertor.tasks.Path.exists", return_value=True
        ), patch(
            "convertor.tasks.delete_file.apply_async"
        ) as mocked_apply_async:
            result = convertor_doc_to_pdf.run("input.docx")

        self.assertEqual(result, converted_path)
        mocked_apply_async.assert_called_once_with(
            args=[converted_path],
            countdown=CONVERTED_FILE_TTL_SECONDS,
        )

    def test_conversion_task_raises_when_output_is_missing(self):
        with patch("convertor.tasks.convert_doc_to_pdf", return_value=None):
            with self.assertRaisesMessage(ValueError, "Conversion failed or the converted file was not created."):
                convertor_doc_to_pdf.run("input.docx")


class DownloadTokenTests(SimpleTestCase):
    def test_download_token_matches_expected_filename(self):
        token = build_download_token("result.pdf")
        self.assertTrue(validate_download_token(token, "result.pdf"))
        self.assertFalse(validate_download_token(token, "other.pdf"))


class FileDownloadViewTests(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = FileDownloadView.as_view()
        self.user = get_user_model().objects.create_user(
            username="tester",
            email="tester@example.com",
            password="secret123",
        )

    def test_download_requires_authentication(self):
        request = self.factory.get("/api/convert/download/result.pdf/")
        response = self.view(request, filename="result.pdf")
        self.assertEqual(response.status_code, 401)

    def test_download_requires_signed_token(self):
        request = self.factory.get("/api/convert/download/result.pdf/")
        force_authenticate(request, user=self.user)
        response = self.view(request, filename="result.pdf")
        self.assertEqual(response.status_code, 400)

    def test_authenticated_download_returns_file_without_deleting_it_immediately(self):
        original_exists = os.path.exists
        original_open = open
        token = build_download_token("result.pdf")

        with tempfile.TemporaryDirectory() as temp_dir:
            converted_dir = os.path.join(temp_dir, "converted_files")
            os.makedirs(converted_dir, exist_ok=True)
            file_name = "result.pdf"
            file_path = os.path.join(converted_dir, file_name)

            with open(file_path, "wb") as fh:
                fh.write(b"pdf-content")

            def remap_path(path):
                return path.replace(CONVERTED_FILES_DIR, converted_dir)

            request = self.factory.get(f"/api/convert/download/{file_name}/", {"token": token})
            force_authenticate(request, user=self.user)

            with patch("convertor.views.os.path.exists", side_effect=lambda path: original_exists(remap_path(path))), patch(
                "convertor.views.open",
                side_effect=lambda path, mode: original_open(remap_path(path), mode),
            ):
                response = self.view(request, filename=file_name)

            self.assertEqual(response.status_code, 200)
            self.assertTrue(os.path.exists(file_path))

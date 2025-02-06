
import os
import subprocess



def convert_doc_to_pdf(input_file_path):
    try:
        output_dir = "/home/jaxon/Python_Projects/convertly/converted_files"
        result = subprocess.run(
            ['soffice',
             '--headless',
             '--nologo',
             '--convert-to', 'pdf:writer_pdf_Export',
             '--outdir', output_dir,
             input_file_path],
            check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        output_file_path = os.path.join(output_dir, os.path.splitext(os.path.basename(input_file_path))[0] + '.pdf')
        print(output_file_path)
        return output_file_path


    except subprocess.CalledProcessError as e:
        print(f"Error during conversion: {e}")
        return None

#
# if __name__ == "__main__":
#     convert_doc_to_pdf("/home/jaxon/Python_Projects/convertly/upload_files/1733989053 (1).docx")
#
# def convert_doc_to_pdf(input_file_path):
#     try:
#         print(input_file_path)
#         filename = os.path.basename(input_file_path)
#         filename_without_doc, extension = os.path.splitext(filename)
#         filename_pdf = filename_without_doc + ".pdf"
#
#         output_dir = f"/home/jaxon/Python_Projects/convertly/converted_files/{filename_pdf}"
#         result = subprocess.run(
#             ["pandoc", input_file_path, "-o", output_dir], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
#         )
#         print(output_dir)
#         return output_dir
#
#     except subprocess.CalledProcessError as e:
#         print(f"Error during conversion: {e}")
#         return None
#
#
# if __name__ == "__main__":
#     # convert_doc_to_pdf("/home/jaxon/Python_Projects/convertly/upload_files/1733989053 (1).docx")
#     convert_doc_to_pdf("/home/jaxon/Python_Projects/convertly/upload_files/upload_files/5mb.docx")





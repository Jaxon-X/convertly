import os
import subprocess

def convert_doc_to_txt(input_file_path):
    try:
        output_dir = "/home/jaxon/Python_Projects/convertly/converted_files"
        result = subprocess.run(
            ['soffice',
             '--headless',
             '--nologo',
             '--convert-to', 'txt',
             '--outdir', output_dir,
             input_file_path],
            check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        print(result)
        output_file_path = os.path.join(output_dir, os.path.splitext(os.path.basename(input_file_path))[0] + '.txt')
        print(output_file_path)
        return output_file_path


    except subprocess.CalledProcessError as e:
        print(f"Error during conversion: {e}")
        return None

if __name__ == "__main__":
    convert_doc_to_txt("/home/jaxon/Python_Projects/convertly/upload_files/upload_files/5mb.docx")
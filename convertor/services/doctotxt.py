import os
import subprocess

def convert_doc_to_txt(input_file_path):
    try:
        output_dir = "/tmp/converted_files"
        os.makedirs(output_dir, exist_ok=True)
        subprocess.run(
            ['soffice',
             '--headless',
             '--nologo',
             '--convert-to', 'txt',
             '--outdir', output_dir,
             input_file_path],
            check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        output_file_path = os.path.join(output_dir, os.path.splitext(os.path.basename(input_file_path))[0] + '.txt')
        return output_file_path


    except subprocess.CalledProcessError as e:
        print(f"Error during conversion: {e}")
        return None


if __name__ == "__main__":
    result = convert_doc_to_txt("/home/jaxon/Downloads/1.docx")
    print(result)


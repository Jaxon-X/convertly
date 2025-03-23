import os
import subprocess


def convert_image_to_pdf(input_file_path):
    try:
        output_dir = "/tmp/converted_files"
        os.makedirs(output_dir, exist_ok=True)
        subprocess.run(
            ['soffice',
             '--headless',
             '--nologo',
             '--convert-to', 'pdf',
             '--outdir', output_dir,
             input_file_path],
            check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        output_file_path = os.path.join(output_dir, os.path.splitext(os.path.basename(input_file_path))[0] + '.pdf')
        return output_file_path


    except subprocess.CalledProcessError as e:
        print(f"Error during conversion: {e}")
        return None


if __name__ == "__main__":
    result = convert_image_to_pdf("/home/jaxon/Downloads/odam.jpg")
    print(result)

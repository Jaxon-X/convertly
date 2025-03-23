
import os
import subprocess



def convert_csv_to_excel(input_file_path):
    try:
        output_dir = "/tmp/converted_files"
        os.makedirs(output_dir, exist_ok=True)
        subprocess.run(
            ['soffice',
             '--headless',
             '--nologo',
             '--convert-to', 'xlsx:Calc MS Excel 2007 XML',
             '--outdir', output_dir,
             input_file_path],
            check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        output_file_path = os.path.join(output_dir, os.path.splitext(os.path.basename(input_file_path))[0] + '.xlsx')
        return output_file_path


    except subprocess.CalledProcessError as e:
        print(f"Error during conversion: {e}")
        return None


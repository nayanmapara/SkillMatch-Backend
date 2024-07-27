import subprocess
import tempfile
import os

def latex_to_pdf(latex_content):
    try:
        with tempfile.NamedTemporaryFile(suffix=".tex", delete=False) as temp_tex_file:
            temp_tex_file.write(latex_content.encode())
            temp_tex_file_path = temp_tex_file.name

        pdf_path = temp_tex_file_path.replace(".tex", ".pdf")

        # Run pdflatex to generate PDF
        subprocess.run(["pdflatex", temp_tex_file_path], check=True)

        with open(pdf_path, 'rb') as pdf_file:
            pdf_data = pdf_file.read()

        return pdf_data
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Failed to generate PDF: {e}")
    finally:
        if os.path.exists(temp_tex_file_path):
            os.remove(temp_tex_file_path)
        if os.path.exists(pdf_path):
            os.remove(pdf_path)

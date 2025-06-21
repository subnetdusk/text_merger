import io
import pandas as pd
from pypdf import PdfWriter, PdfReader
import docx
from markdown_it import MarkdownIt
from bs4 import BeautifulSoup
from xhtml2pdf import pisa

def merge_as_txt(files):
    output_string = io.StringIO()
    for file in files:
        file.seek(0)
        file_extension = file.name.split('.')[-1].lower()
        content = ""
        try:
            if file_extension == 'txt':
                content = file.read().decode('utf-8')
            elif file_extension == 'pdf':
                reader = PdfReader(file)
                for page in reader.pages:
                    content += page.extract_text() + "\n"
            elif file_extension == 'docx':
                doc = docx.Document(file)
                for para in doc.paragraphs:
                    content += para.text + "\n"
            else:
                content = file.read().decode('utf-8', errors='ignore')

            output_string.write(content)
            output_string.write("\n\n--- End of File: {} ---\n\n".format(file.name))
        except Exception as e:
            output_string.write("\n\n--- Could not process file: {} (Error: {}) ---\n\n".format(file.name, e))
    return output_string.getvalue().encode('utf-8')

def merge_as_csv(files):
    dataframes = []
    ignored_files = []
    for file in files:
        file.seek(0)
        if file.name.endswith('.csv'):
            try:
                df = pd.read_csv(file)
                dataframes.append(df)
            except Exception:
                ignored_files.append(file.name)
        else:
            ignored_files.append(file.name)
    
    if not dataframes:
        return None, ignored_files

    merged_df = pd.concat(dataframes, ignore_index=True)
    csv_buffer = io.StringIO()
    merged_df.to_csv(csv_buffer, index=False)
    return csv_buffer.getvalue().encode('utf-Tf-8'), ignored_files

def _convert_to_html_fragment(file):
    file.seek(0)
    file_extension = file.name.split('.')[-1].lower()
    
    if file_extension == 'html':
        soup = BeautifulSoup(file.read(), 'lxml')
        return str(soup.body) if soup.body else ''
    elif file_extension == 'md':
        md = MarkdownIt()
        return md.render(file.read().decode('utf-8'))
    elif file_extension == 'csv':
        df = pd.read_csv(file)
        return df.to_html(index=False)
    elif file_extension == 'txt':
        content = file.read().decode('utf-8')
        return f'<pre>{content}</pre>'
    elif file_extension == 'docx':
        doc = docx.Document(file)
        content = "\n".join([para.text for para in doc.paragraphs])
        return f'<div>{"<p>" + content.replace(chr(10), "</p><p>") + "</p>"}</div>'
    elif file_extension == 'pdf':
        reader = PdfReader(file)
        content = "".join([page.extract_text() for page in reader.pages])
        return f'<div>{"<p>" + content.replace(chr(10), "</p><p>") + "</p>"}</div>'
    return ""

def merge_as_html(files):
    html_fragments = []
    for file in files:
        try:
            html_fragments.append(_convert_to_html_fragment(file))
        except Exception:
            html_fragments.append(f"<hr><p>Could not process file: {file.name}</p>")

    full_html_content = "<hr>".join(html_fragments)
    
    final_html = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Merged Document</title>
        <style>
            body {{ font-family: sans-serif; margin: 2em; }}
            table {{ border-collapse: collapse; width: 100%; }}
            th, td {{ border: 1px solid #dddddd; text-align: left; padding: 8px; }}
            th {{ background-color: #f2f2f2; }}
            hr {{ margin: 2em 0; border: 1px solid #ccc; }}
            pre {{ background-color: #f5f5f5; padding: 1em; white-space: pre-wrap; word-wrap: break-word; }}
        </style>
    </head>
    <body>
        {full_html_content}
    </body>
    </html>
    """
    return final_html.encode('utf-8')

def merge_as_pdf(files):
    pdf_files = [f for f in files if f.name.endswith('.pdf')]
    other_files = [f for f in files if not f.name.endswith('.pdf')]
    
    writer = PdfWriter()
    
    # First, merge existing PDFs
    for pdf_file in pdf_files:
        pdf_file.seek(0)
        reader = PdfReader(pdf_file)
        for page in reader.pages:
            writer.add_page(page)

    # Then, convert other files to PDF and merge
    if other_files:
        html_content = merge_as_html(other_files)
        
        pdf_output = io.BytesIO()
        pisa_status = pisa.CreatePDF(io.BytesIO(html_content), dest=pdf_output)
        
        if not pisa_status.err:
            pdf_output.seek(0)
            html_as_pdf_reader = PdfReader(pdf_output)
            for page in html_as_pdf_reader.pages:
                writer.add_page(page)

    pdf_bytes_io = io.BytesIO()
    writer.write(pdf_bytes_io)
    return pdf_bytes_io.getvalue()

from mergers import merger_logic

def determine_output_format(files, force_pdf):
    if force_pdf:
        return 'pdf'
    
    extensions = {f.name.split('.')[-1].lower() for f in files}
    
    if 'pdf' in extensions:
        return 'pdf'
    if 'html' in extensions or 'md' in extensions:
        return 'html'
    if 'docx' in extensions:
        return 'html' # Promote to HTML for rich text
    if 'csv' in extensions:
        # If only CSV and TXT are present, prefer CSV
        other_ext = extensions - {'csv', 'txt'}
        if not other_ext:
            return 'csv'
        else: # If other complex types are there, promote to html
             return 'html'
    return 'txt'

def process_files(files, force_pdf):
    output_format = determine_output_format(files, force_pdf)
    
    filename = f"merged_document.{output_format}"
    warnings = None
    
    if output_format == 'pdf':
        merged_data = merger_logic.merge_as_pdf(files)
    elif output_format == 'html':
        merged_data = merger_logic.merge_as_html(files)
    elif output_format == 'csv':
        merged_data, ignored = merger_logic.merge_as_csv(files)
        if ignored:
            warnings = f"The following files were ignored to preserve the CSV format: {', '.join(ignored)}"
        if merged_data is None:
            return None, "No CSV files found to merge.", None
    else: # txt
        merged_data = merger_logic.merge_as_txt(files)
        
    return merged_data, filename, warnings

import streamlit as st
from utils import file_handler
import time

st.set_page_config(
    page_title="File Merger App",
    page_icon="🔗",
    layout="centered"
)

# This key will be used to reset the file_uploader widget
if 'uploader_key' not in st.session_state:
    st.session_state.uploader_key = 0

st.title("🔗 File Merger Application")
st.write(
    "Upload your files (TXT, PDF, DOCX, etc.), "
    "and merge them into a single document."
)

st.header("1. Upload Your Files")

uploaded_files = st.file_uploader(
    "Choose files to merge",
    accept_multiple_files=True,
    type=['txt', 'pdf', 'docx', 'md', 'html', 'csv'],
    key=f"file_uploader_{st.session_state.uploader_key}" # Use the key from session state
)

# --- Merger Options Section ---
st.header("2. Set Your Options")

force_pdf_output = st.checkbox(
    "Force final output as a PDF file",
    help="If selected, all uploaded files will be converted and merged into a single PDF."
)

st.header("3. Merge & Download")

if uploaded_files:
    st.info(f"You have uploaded {len(uploaded_files)} files. The merging order is based on the upload sequence.")

    for file in uploaded_files:
        st.write(f"- `{file.name}`")

    col1, col2 = st.columns([1, 1])

    with col1:
        if st.button("Merge Files", type="primary", use_container_width=True):
            with st.spinner("Processing files... Please wait."):
                try:
                    merged_data, output_filename, warnings = file_handler.process_files(
                        uploaded_files, force_pdf_output
                    )
                    
                    if warnings:
                        st.warning(warnings)

                    if merged_data:
                        st.success("Files merged successfully!")
                        # Store result in session state to survive the reset button click
                        st.session_state.merged_data = merged_data
                        st.session_state.output_filename = output_filename
                    else:
                        st.error("Could not merge the files. Please check the file types or their content.")

                except Exception as e:
                    st.error(f"An error occurred: {e}")

    with col2:
        # The reset button clears the file uploader by incrementing its key
        if st.button("Reset", use_container_width=True):
            st.session_state.uploader_key += 1
            # Also clear any previous download buttons
            if 'merged_data' in st.session_state:
                del st.session_state['merged_data']
            st.rerun()

    if 'merged_data' in st.session_state and st.session_state.merged_data is not None:
        st.download_button(
            label=f"Download {st.session_state.output_filename}",
            data=st.session_state.merged_data,
            file_name=st.session_state.output_filename,
            mime=f'application/{st.session_state.output_filename.split(".")[-1]}',
            use_container_width=True
        )

else:
    st.warning("Waiting for files to be uploaded...")


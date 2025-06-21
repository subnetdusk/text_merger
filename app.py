import streamlit as st
from utils import file_handler

st.set_page_config(
    page_title="File Merger App",
    page_icon="🔗",
    layout="centered"
)

st.title("🔗 File Merger Application")
st.write(
    "Upload your files (TXT, PDF, DOCX, etc.), "
    "and merge them into a single document."
)

st.header("1. Upload Your Files")

uploaded_files = st.file_uploader(
    "Choose files to merge",
    accept_multiple_files=True,
    type=['txt', 'pdf', 'docx', 'md', 'html', 'csv']
)

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

    if st.button("Merge Files", type="primary"):
        with st.spinner("Processing files... Please wait."):
            try:
                merged_data, output_filename, warnings = file_handler.process_files(
                    uploaded_files, force_pdf_output
                )
                
                if warnings:
                    st.warning(warnings)

                if merged_data:
                    st.success("Files merged successfully!")
                    st.download_button(
                        label=f"Download {output_filename}",
                        data=merged_data,
                        file_name=output_filename,
                        mime=f'application/{output_filename.split(".")[-1]}'
                    )
                else:
                    st.error("Could not merge the files. Please check the file types or their content.")

            except Exception as e:
                st.error(f"An error occurred: {e}")
else:
    st.warning("Waiting for files to be uploaded...")

st.markdown("---")
st.write("Made with ❤️ using Streamlit")

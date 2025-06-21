import streamlit as st
import pandas as pd # We'll use this later, but it's good to have

st.set_page_config(
    page_title="File Merger App",
    page_icon="🔗",
    layout="centered"
)

st.title("🔗 File Merger Application")
st.write(
    "Upload your files (TXT, PDF, DOCX, etc.), "
    "reorder them if needed, and merge them into a single document."
)

st.header("1. Upload Your Files")

uploaded_files = st.file_uploader(
    "Choose files to merge",
    accept_multiple_files=True,
    # We will specify the file types later
    # type=['txt', 'pdf', 'docx', 'md', 'html', 'csv']
)

st.header("2. Set Your Options")

force_pdf_output = st.checkbox(
    "Force final output as a PDF file",
    help="If selected, all uploaded files will be converted and merged into a single PDF, regardless of their original format."
)

st.header("3. Merge & Download")

if uploaded_files:
    # This is a temporary message. The ability to reorder is a future step.
    st.info(f"You have uploaded {len(uploaded_files)} files. The merging order will be based on the upload sequence.")

    for file in uploaded_files:
        st.write(f"- `{file.name}` ({round(file.size / 1024, 2)} KB)")

    if st.button("Merge Files", type="primary"):
        st.success("Merging logic to be implemented!")
        if force_pdf_output:
            st.write("User has requested a PDF output.")
        else:
            st.write("The output will follow the standard format promotion logic.")

else:
    st.warning("Waiting for files to be uploaded...")

st.markdown("---")
st.write("Made with ❤️ using Streamlit")

import streamlit as st
from PyPDF2 import PdfReader, PdfWriter
import os

def merge_pdfs(pdf1, pdf2):
    pdf_writer = PdfWriter()
    
    for pdf in [pdf1, pdf2]:
        pdf_reader = PdfReader(pdf)
        for page in range(len(pdf_reader.pages)):
            pdf_writer.add_page(pdf_reader.pages[page])
    
    merged_pdf_path = "merged.pdf"
    with open(merged_pdf_path, "wb") as out:
        pdf_writer.write(out)
    
    return merged_pdf_path

st.title("PDF Merger")
st.write("Upload two PDF files to merge them into a single PDF.")

pdf_file1 = st.file_uploader("Choose the first PDF file", type="pdf")
pdf_file2 = st.file_uploader("Choose the second PDF file", type="pdf")

if st.button("Merge PDFs"):
    if pdf_file1 and pdf_file2:
        merged_pdf_path = merge_pdfs(pdf_file1, pdf_file2)
        with open(merged_pdf_path, "rb") as f:
            st.download_button("Download Merged PDF", f, file_name="merged.pdf")
        os.remove(merged_pdf_path)
    else:
        st.error("Please upload both PDF files.")
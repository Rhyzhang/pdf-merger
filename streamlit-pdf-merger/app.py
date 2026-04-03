import streamlit as st
from PyPDF2 import PdfReader, PdfWriter
from PIL import Image
import io
import base64

# --- HELPER FUNCTIONS ---

def merge_pdfs(pdf1, pdf2):
    pdf_writer = PdfWriter()
    
    for pdf in [pdf1, pdf2]:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            pdf_writer.add_page(page)
            
    out_pdf = io.BytesIO()
    pdf_writer.write(out_pdf)
    out_pdf.seek(0) 
    return out_pdf

def images_to_pdf(image_files):
    images = []
    for img_file in image_files:
        img = Image.open(img_file)
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")
        images.append(img)
        
    out_pdf = io.BytesIO()
    if images:
        images[0].save(out_pdf, format="PDF", save_all=True, append_images=images[1:])
    out_pdf.seek(0)
    return out_pdf

def crop_pdf(pdf_file, left, right, top, bottom):
    pdf_reader = PdfReader(pdf_file)
    pdf_writer = PdfWriter()
    
    for page in pdf_reader.pages:
        upper_right = page.mediabox.upper_right
        lower_left = page.mediabox.lower_left
        
        new_lower_left = (lower_left[0] + left, lower_left[1] + bottom)
        new_upper_right = (upper_right[0] - right, upper_right[1] - top)
        
        page.mediabox.lower_left = new_lower_left
        page.mediabox.upper_right = new_upper_right
        
        pdf_writer.add_page(page)
        
    out_pdf = io.BytesIO()
    pdf_writer.write(out_pdf)
    out_pdf.seek(0)
    return out_pdf

def display_pdf(pdf_stream, height=600):
    """Encodes a PDF byte stream to base64 and displays it in an iframe."""
    base64_pdf = base64.b64encode(pdf_stream.getvalue()).decode('utf-8')
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="{height}" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)

# --- APP UI ---

st.set_page_config(page_title="PDF Toolkit", layout="wide") # Switched to wide layout to better accommodate previews

st.sidebar.title("PDF Toolkit")
tool = st.sidebar.radio("Select a Tool:", ["Merge PDFs", "PNG to PDF", "Crop PDF margins"])

# --- TOOL 1: MERGER ---
if tool == "Merge PDFs":
    st.title("PDF Merger")
    st.write("Upload two PDF files to merge them into a single PDF.")

    col1, col2 = st.columns(2)
    with col1:
        pdf_file1 = st.file_uploader("Choose the first PDF file", type="pdf")
    with col2:
        pdf_file2 = st.file_uploader("Choose the second PDF file", type="pdf")

    if st.button("Merge PDFs"):
        if pdf_file1 and pdf_file2:
            merged_pdf_stream = merge_pdfs(pdf_file1, pdf_file2)
            st.success("Successfully merged! Scroll down to preview.")
            
            st.download_button(
                label="Download Merged PDF", 
                data=merged_pdf_stream, 
                file_name="merged.pdf",
                mime="application/pdf"
            )
            
            st.subheader("Merged PDF Preview")
            display_pdf(merged_pdf_stream)
        else:
            st.error("Please upload both PDF files.")

# --- TOOL 2: PNG TO PDF ---
elif tool == "PNG to PDF":
    st.title("Image to PDF Converter")
    st.write("Upload one or more PNG/JPG images to convert them into a single PDF.")
    
    uploaded_images = st.file_uploader("Choose images", type=["png", "jpg", "jpeg"], accept_multiple_files=True)
    
    if uploaded_images:
        st.write("### Image Preview")
        # Display image previews in a row using columns
        cols = st.columns(min(len(uploaded_images), 5)) 
        for i, img_file in enumerate(uploaded_images[:5]): 
            with cols[i]:
                st.image(img_file, use_container_width=True, caption=img_file.name)
        if len(uploaded_images) > 5:
            st.write(f"...and {len(uploaded_images) - 5} more images.")

    if st.button("Convert to PDF"):
        if uploaded_images:
            converted_pdf_stream = images_to_pdf(uploaded_images)
            st.success("Successfully converted! Scroll down to preview the PDF.")
            
            st.download_button(
                label="Download Image PDF",
                data=converted_pdf_stream,
                file_name="images_converted.pdf",
                mime="application/pdf"
            )
            
            st.subheader("Generated PDF Preview")
            display_pdf(converted_pdf_stream)
        else:
            st.error("Please upload at least one image.")

# --- TOOL 3: CROP PDF ---
elif tool == "Crop PDF margins":
    st.title("PDF Cropper")
    st.write("Upload a PDF and specify margins to crop off the edges of all pages.")
    
    pdf_to_crop = st.file_uploader("Choose a PDF file to crop", type="pdf")
    
    col_t, col_b, col_l, col_r = st.columns(4)
    with col_t:
        crop_top = st.number_input("Top margin", min_value=0, max_value=500, value=0)
    with col_b:
        crop_bottom = st.number_input("Bottom margin", min_value=0, max_value=500, value=0)
    with col_l:
        crop_left = st.number_input("Left margin", min_value=0, max_value=500, value=0)
    with col_r:
        crop_right = st.number_input("Right margin", min_value=0, max_value=500, value=0)
    
    if pdf_to_crop:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Original PDF Preview")
            # We copy the stream so we don't interfere with the crop function's read position
            pdf_bytes = io.BytesIO(pdf_to_crop.getvalue())
            display_pdf(pdf_bytes, height=500)
            
        with col2:
            st.subheader("Cropped PDF Preview")
            if st.button("Generate Crop Preview"):
                cropped_pdf_stream = crop_pdf(pdf_to_crop, crop_left, crop_right, crop_top, crop_bottom)
                display_pdf(cropped_pdf_stream, height=500)
                
                st.download_button(
                    label="Download Cropped PDF",
                    data=cropped_pdf_stream,
                    file_name="cropped.pdf",
                    mime="application/pdf"
                )
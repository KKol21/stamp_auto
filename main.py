import streamlit as st
import fitz  # PyMuPDF
import io

# === PRESET TEXT TO WRITE ===
PRESET_TEXT = """Boliden Commercial AB/NO
Eitrheimsneset 1, 5750 Odda, Norge
VAT NO987485752MVA"""


def edit_lower_left(pdf_bytes, new_text):
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    
    for page in doc:
        rect = page.rect
        margin_x = 0  # Distance from left
        margin_y = 0  # Distance from bottom
        width = 150
        height = 50
        
        erase_rect = fitz.Rect(margin_x, margin_y - height, margin_x + width, margin_y)
        
        # Redact old stamp
        page.add_redact_annot(rect, fill=(1, 1, 1))
        page.apply_redactions()
        
        # Overwrite with new text
        page.insert_textbox(
            erase_rect,
            new_text,
            fontsize=10,
            fontname="helv",
            color=(0, 0, 0),
            align=fitz.TEXT_ALIGN_LEFT
        )

    # Save to BytesIO
    output = io.BytesIO()
    doc.save(output)
    doc.close()
    output.seek(0)
    return output

# === Streamlit UI ===
st.title("PDF Text Overwriter (Lower-Left Corner)")
st.write("This tool erases and replaces the lower-left corner of each page in your PDF.")

uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])

if uploaded_file:
    if st.button("Process PDF"):
        modified_pdf = edit_lower_left(uploaded_file.read(), PRESET_TEXT)
        st.success("PDF modified successfully!")

        st.download_button(
            label="Download Modified PDF",
            data=modified_pdf,
            file_name="modified.pdf",
            mime="application/pdf"
        )

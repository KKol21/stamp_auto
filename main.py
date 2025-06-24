import streamlit as st
import fitz  # PyMuPDF
import io

# Fixed text
old_text = """Boliden Commercial AB
Box 750, 101 35 Stockholm, Sweden
Tel. +46 8 610 15 00, Fax. +46 8 610 15 50
Org.nr 556158-2205
Godkänd för F-skatt"""

new_text = """Boliden Commercial AB/NO
Eitrheimsneset 1, 5750 Odda, Norge
VAT NO987485752MVA"""

def replace_fixed_text(file_bytes):
    doc = fitz.open(stream=file_bytes, filetype="pdf")

    for page in doc:
        text_to_delete = page.search_for(old_text, quads=True)
        if text_to_delete:
            for quad in text_to_delete:
                page.add_redact_annot(quad)
            page.apply_redactions()

            # Merge quads into bounding box
            all_rects = [q.rect for q in text_to_delete]
            x0 = min(r.x0 for r in all_rects)
            y0 = min(r.y0 for r in all_rects)
            x1 = max(r.x1 for r in all_rects)
            y1 = max(r.y1 for r in all_rects)
            full_rect = fitz.Rect(x0, y0, x1, y1)

            page.insert_textbox(
                full_rect,
                new_text,
                fontname="helv",
                fontsize=10,
                color=(0, 0, 0),
                align=fitz.TEXT_ALIGN_LEFT
            )

    output_bytes = io.BytesIO()
    doc.save(output_bytes)
    doc.close()
    return output_bytes

# Streamlit UI
st.title("PDF Footer Replacer")
st.caption("Automatically replaces the Boliden footer block with updated Norwegian address.")

uploaded_file = st.file_uploader("Upload PDF", type="pdf")

if uploaded_file:
    result = replace_fixed_text(uploaded_file.read())
    st.success("✅ Replacement complete!")
    st.download_button("Download Modified PDF", result.getvalue(), file_name="output.pdf")

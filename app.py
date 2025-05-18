import streamlit as st
from PIL import Image
import easyocr

st.set_page_config(page_title="📷 English Text Extractor", layout="centered")
st.title("📤 Upload an Image to Extract English Text")

# Upload image only (no camera yet)
image = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

# Cache the EasyOCR reader so it doesn’t reload every time
@st.cache_resource
def get_reader():
    return easyocr.Reader(['en'], gpu=False)

reader = get_reader()

# When image is uploaded
if image is not None:
    img = Image.open(image)
    st.image(img, caption="Uploaded Image", use_column_width=True)

    with st.spinner("🔍 Extracting text..."):
        result = reader.readtext(img, detail=0)
        extracted_text = "\n".join(result)

    st.subheader("📝 Extracted Text")
    st.write(extracted_text)
    
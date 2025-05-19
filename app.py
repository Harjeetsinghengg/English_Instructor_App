import streamlit as st
from PIL import Image
import easyocr
import requests

st.set_page_config(page_title="📷 Grammar Checker from Image", layout="centered")
st.title("📸 English Grammar Feedback from Image")

# 📸 Allow both camera and file upload
image = st.camera_input("Take a photo") or st.file_uploader("Or upload an image", type=["png", "jpg", "jpeg"])

# 🧠 Cached OCR reader
@st.cache_resource
def get_reader():
    return easyocr.Reader(['en'], gpu=False)

reader = get_reader()

# ✍️ Grammar checking via LanguageTool API
def check_grammar(text):
    url = "https://api.languagetoolplus.com/v2/check"
    data = {
        "text": text,
        "language": "en-US"
    }
    try:
        response = requests.post(url, data=data, timeout=10)
        response.raise_for_status()
        return response.json().get("matches", [])
    except Exception as e:
        st.error(f"❌ Error during grammar check: {e}")
        return []

# 🔁 Main logic
if image is not None:
    img = Image.open(image)
    st.image(img, caption="🖼 Image Preview", use_column_width=True)

    with st.spinner("🔍 Extracting text..."):
        result = reader.readtext(img, detail=0)
        extracted_text = "\n".join(result)

    st.subheader("📝 Extracted Text")
    st.write(extracted_text)

    if extracted_text.strip():
        with st.spinner("🔎 Checking grammar..."):
            grammar_issues = check_grammar(extracted_text)
            num_errors = len(grammar_issues)
            score = max(0, 10 - num_errors)

            st.subheader("📊 Feedback Summary")
            st.markdown(f"**Grammar Score:** `{score}/10`")
            st.markdown(f"**Issues Found:** `{num_errors}`")

            if grammar_issues:
                st.markdown("### ❌ Grammar Mistakes and Suggestions")
                for issue in grammar_issues:
                    message = issue["message"]
                    context = issue["context"]["text"]
                    suggestions = ", ".join([r["value"] for r in issue.get("replacements", [])]) or "No suggestion"

                    st.markdown(f"""
                    - 🔴 **Issue**: {message}  
                      🔍 **Text**: `{context.strip()}`  
                      ✅ **Suggestion**: `{suggestions}`
                    """)
            else:
                st.success("🎉 No grammar issues found. Well written!")
    else:
        st.warning("⚠️ No readable English text found in the image.")

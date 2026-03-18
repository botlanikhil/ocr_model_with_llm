import os
import streamlit as st
import json
from paddleocr import PaddleOCR
from groq import Groq
from dotenv import load_dotenv
import numpy as np
from PIL import Image


# Load API

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# OCR (cached)

@st.cache_resource
def load_ocr():
    return PaddleOCR(lang='en')


def run_ocr(images):
    ocr = load_ocr()
    all_text = []

    for file in images:

        # Convert uploaded file → PIL → numpy
        image = Image.open(file).convert("RGB")
        img_array = np.array(image)

        result = ocr.ocr(img_array)

        if result and result[0]:
            for line in result[0]:
                all_text.append(line[1][0])

    return all_text, " ".join(all_text)


# LLM

def extract_info(text):

    prompt = f"""
You are an expert in reconstructing OCR text from medicine packaging.

Task:
- The input text is extracted from multiple images of a pill box.
- The text may be unordered, broken, duplicated, or noisy.

Your job:
1. Reorder the text into a logical reading order.
2. Merge broken words and sentences.
3. Remove duplicate or irrelevant OCR noise.
4. Preserve ALL meaningful information.
5. Create a clean, readable paragraph.

Then:
6. Extract structured drug information:
   - medicine_name
   - dosage
   - batch_number
   - expiry_date
   - manufacturer
   - composition
   - usage
   - warnings
   - storage

Rules:
- Do NOT lose important information
- Do NOT hallucinate missing data
- If something is not present → return null
- Return ONLY JSON (no explanation)

Output format (STRICT JSON ONLY):

{{
  "full_text": "clean reconstructed sentence of the medicine packaging",
  "medicine_name": "...",
  "dosage": "...",
  "batch_number": "...",
  "expiry_date": "...",
  "manufacturer": "...",
  "composition": "...",
  "usage": "...",
  "warnings": "...",
  "storage": "..."
}}

OCR TEXT:
{full_text}
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content



# UI

st.set_page_config(page_title="💊 Drug Analyzer", layout="wide")

st.title("💊 Smart Drug Information Extractor")
st.caption("Upload images ")

uploaded_files = st.file_uploader(
    "📤 Upload pill images",
    type=["jpg", "png", "jpeg"],
    accept_multiple_files=True
)

if uploaded_files :
    st.warning("uploaded")
    
    if st.button(" Analyze"):

        with st.spinner(" Running OCR..."):
            raw_text_list, full_text = run_ocr(uploaded_files)

        with st.spinner(" Extracting Info..."):
            output = extract_info(full_text)

        st.success("✅ Done")
        # SHOW OCR TEXT
       
        st.subheader("📜 OCR Extracted Text")

        with st.expander("View Full OCR Text"):
            st.text_area("All Extracted Text", full_text, height=200)
        
    
        # SHOW STRUCTURED INFO
        
        st.subheader(" Drug Information")

        try:
            data = json.loads(output)

            col1, col2 = st.columns(2)

            with col1:
                st.info(f"**Name:** {data.get('medicine_name')}")
                st.info(f"**Dosage:** {data.get('dosage')}")
                st.info(f"**Batch:** {data.get('batch_number')}")
                st.info(f"**Expiry:** {data.get('expiry_date')}")

            with col2:
                st.info(f"**Manufacturer:** {data.get('manufacturer')}")
                st.info(f"**Composition:** {data.get('composition')}")
                st.info(f"**Usage:** {data.get('usage')}")
                st.info(f"**Storage:** {data.get('storage')}")

            st.warning(f" Warnings: {data.get('warnings')}")
            st.write(f" Other Info: {data.get('other_details')}")

        except:
            st.code(output)
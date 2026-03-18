# ocr_model_with_llm
# Pill OCR & Drug Info Extractor

A Streamlit web app that lets users upload photos of medicine packaging, automatically runs OCR to read text, and uses an LLM to reconstruct and extract detailed drug information.  
Designed for clean, structured outputs and an easy, modern UI—no need to pre‑save JSON files or manage folders manually.

---

## 🚀 What this project does

- **Upload images** of pill boxes or medicine packaging.
- **Run OCR** on the images to extract text.
- **Clean, reorder, and merge** OCR output so it reads like real packaging.
- **Extract structured drug details** such as:
  - Medicine name, dosage, batch number, expiry, manufacturer, composition, usage, warnings, storage, and more.
- Show both the **full extracted text** and **clean structured info** in the UI.
- Built with **Streamlit**, **PaddleOCR**, and a **Groq LLM** for high‑quality reconstruction and extraction.

---

## 🧩 Key features

- **Single‑page web UI**: upload and analyze in one place.
- **Robust text reconstruction**: handles unordered, broken, or noisy OCR text.
- **Strict JSON output**: ensures the app returns clean, parseable data.
- **Expandable**: easy to add more fields, change prompt, or plug in a different model.
- **No JSON files needed**: data flows in memory from OCR to LLM to UI.

---

## 🛠️ Tech stack

- Python
- Streamlit for the UI
- PaddleOCR for on‑device OCR
- Groq LLM for text reconstruction and extraction
- `python-dotenv` for securely loading API keys

---


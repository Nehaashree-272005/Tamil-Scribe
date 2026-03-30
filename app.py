import streamlit as st
from io import StringIO
import docx2txt
import pdfplumber
import re
from google import genai
from sentence_transformers import SentenceTransformer, util
import torch
import os
from dotenv import load_dotenv

# -------------------------------------------------------
# 📌 Streamlit Config (MUST BE FIRST)
# -------------------------------------------------------
st.set_page_config(page_title="Tamil-Scribe", page_icon="📝")

# -------------------------------------------------------
# 🔑 Load API Key
# -------------------------------------------------------
load_dotenv()

api_key = None

try:
    api_key = st.secrets["GEMINI_API_KEY"]
except Exception:
    api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("❌ GEMINI_API_KEY not found. Please set it in your .env file or Streamlit secrets.")
    st.stop()

# ✅ NEW Gemini Client
client = genai.Client(api_key=api_key)

# -------------------------------------------------------
# ✅ Sentence Transformer (fallback)
# -------------------------------------------------------
sentence_model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")

# -------------------------------------------------------
# 🔧 Utility Functions
# -------------------------------------------------------
def extract_text_from_file(uploaded_file):
    if uploaded_file.type == "text/plain":
        return StringIO(uploaded_file.getvalue().decode("utf-8")).read()

    elif uploaded_file.type.endswith("wordprocessingml.document"):
        return docx2txt.process(uploaded_file)

    elif uploaded_file.type == "application/pdf":
        text = ""
        with pdfplumber.open(uploaded_file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text

    else:
        st.error("Unsupported file format.")
        return ""


def extract_key_sentences_global(text, n=5):
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())

    if len(sentences) <= n:
        return sentences

    embeddings = sentence_model.encode(sentences, convert_to_tensor=True)
    doc_embedding = sentence_model.encode(text, convert_to_tensor=True)

    scores = util.pytorch_cos_sim(embeddings, doc_embedding).squeeze()
    top_idxs = torch.topk(scores, k=n).indices

    return [sentences[i] for i in sorted(top_idxs)]


def detect_language(text):
    tamil_chars = re.findall(r'[\u0B80-\u0BFF]', text)
    return "ta" if len(tamil_chars) > 10 else "en"


# -------------------------------------------------------
# 💡 Gemini Summarization (NEW SDK)
# -------------------------------------------------------
def summarize_with_gemini(text, lang="ta"):
    if lang == "ta":
        prompt = f"""
Summarize the following text in Tamil.
Keep key ideas, important facts, and dates.
Use bullet points.

{text}
"""
    else:
        prompt = f"""
Summarize the following English text clearly:

{text}
"""

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )

        return response.text.strip() if response.text else ""

    except Exception as e:
        st.warning(f"Model Summarization failed: {e}")
        return ""


# -------------------------------------------------------
# 🔁 Fallback Summarization
# -------------------------------------------------------
def summarize_with_fallback(text, n=5):
    st.warning("⚠️ Gemini failed. Using fallback summarization.")

    summary_points = extract_key_sentences_global(text, n=n)

    seen = set()
    unique_summary = []

    for point in summary_points:
        clean = point.strip()
        if clean and clean not in seen:
            seen.add(clean)
            unique_summary.append(clean)

    return unique_summary


# -------------------------------------------------------
# 🎨 Streamlit UI
# -------------------------------------------------------
st.title("📝 Tamil Scribe - AI Summarizer")

method = st.radio("Choose input method:", ["📝 Type Text", "📄 Upload File"])
text_input = ""

if method == "📝 Type Text":
    text_input = st.text_area("Enter Tamil or English text:", height=200)

else:
    uploaded = st.file_uploader("Upload a file (txt, docx, pdf)", type=["txt", "docx", "pdf"])

    if uploaded:
        text_input = extract_text_from_file(uploaded)
        st.success("✅ Text successfully extracted!")

# -------------------------------------------------------
# 🚀 Summarization Button
# -------------------------------------------------------
if st.button("Summarize") and text_input.strip():

    st.subheader("🔍 Original Text")
    st.write(text_input)

    lang = detect_language(text_input)
    st.info(f"🌐 Detected Language: {'Tamil' if lang == 'ta' else 'English'}")

    with st.spinner("Summarizing..."):
        gemini_summary = summarize_with_gemini(text_input, lang)

    if gemini_summary:
        st.subheader("✍ Summary")
        st.write(gemini_summary)

        st.info(f"📏 Input Length: {len(text_input.split())} words")
        st.info(f"📄 Summary Length: {len(gemini_summary.split())} words")

        ratio = round(len(text_input.split()) / max(1, len(gemini_summary.split())), 2)
        st.success(f"📊 Compression Ratio: 1 : {ratio}")

    else:
        fallback_summary = summarize_with_fallback(text_input)

        st.subheader("📃 Fallback Summary")
        for point in fallback_summary:
            st.markdown(f"- {point}")

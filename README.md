# 📝 Tamil Scribe — AI-Powered Summarizer

A bilingual (Tamil + English) text summarizer built with **Streamlit** and **Google Gemini 1.5 Pro**. Supports typed text, `.txt`, `.docx`, and `.pdf` file uploads. Falls back to extractive summarization when the AI model is unavailable.

---

## 🚀 Features

- 🌐 Auto-detects Tamil or English input
- 📄 Supports file upload: `.txt`, `.docx`, `.pdf`
- 🤖 Gemini 1.5 Pro for abstractive summarization
- 🔁 Sentence-transformer fallback if Gemini fails
- 📊 Shows compression ratio and word counts

---

## 📁 Project Structure

```
tamil-scribe/
│
├── app.py                    ← Main Streamlit app
├── requirements.txt          ← Python dependencies
├── .env.example              ← Template for your .env file
├── .gitignore                ← Files Git will ignore
├── README.md                 ← This file
│
├── .env                      ← ❌ You create this (never commit!)
│
└── .streamlit/
    ├── config.toml           ← Streamlit theme config
    └── secrets.toml          ← ❌ You create this (never commit!)
```

---

## ⚙️ Local Setup — Step by Step

### Step 1: Clone or download the project

```bash
git clone https://github.com/yourusername/tamil-scribe.git
cd tamil-scribe
```

### Step 2: Create a virtual environment

```bash
python -m venv venv
```

### Step 3: Activate the virtual environment

**Windows:**
```bash
venv\Scripts\activate
```

**Mac / Linux:**
```bash
source venv/bin/activate
```

You'll see `(venv)` in your terminal — that means it's active.

### Step 4: Install dependencies

```bash
pip install -r requirements.txt
```

### Step 5: Set up your API key

1. Go to [aistudio.google.com](https://aistudio.google.com)
2. Click **Get API Key** → **Create API Key**
3. Copy the key

Create a file named `.env` in the project root:

```
GEMINI_API_KEY=your_actual_key_here
```

> ⚠️ Never share this file or commit it to GitHub.

### Step 6: Run the app

```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

---

## 🔐 API Key Security Rules

| ✅ Safe | ❌ Never Do |
|---|---|
| Store in `.env` locally | Hardcode in `app.py` |
| Use `st.secrets` on cloud | Push `.env` to GitHub |
| Add `.env` to `.gitignore` | Share in chat or email |

---

## ☁️ Deploying to Streamlit Community Cloud

### Step 1: Push your code to GitHub

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/yourusername/tamil-scribe.git
git push -u origin main
```

> Note: `.env` and `secrets.toml` are in `.gitignore` so they won't be pushed. Good!

### Step 2: Go to Streamlit Cloud

1. Visit [share.streamlit.io](https://share.streamlit.io)
2. Sign in with your **GitHub account**
3. Click **"New app"**

### Step 3: Configure the app

- **Repository:** `yourusername/tamil-scribe`
- **Branch:** `main`
- **Main file path:** `app.py`

### Step 4: Add your API key as a Secret

1. Click **"Advanced settings"** before deploying
2. In the **Secrets** section, paste this:

```toml
GEMINI_API_KEY = "your_actual_key_here"
```

3. Click **Deploy!**

Your app will be live at:
```
https://yourusername-tamil-scribe-app-xxxx.streamlit.app
```

---

## 🔄 Updating Your App After Deployment

Whenever you make changes:

```bash
git add .
git commit -m "describe what you changed"
git push
```

Streamlit Cloud **auto-redeploys** whenever you push to GitHub.

---

## 🧪 Tech Stack

| Tool | Purpose |
|---|---|
| Streamlit | Web UI framework |
| Google Gemini 1.5 Pro | AI summarization |
| sentence-transformers | Fallback extractive summarization |
| pdfplumber | PDF text extraction |
| docx2txt | Word document extraction |
| deep-translator | Language translation utilities |
| python-dotenv | Local `.env` loading |

---

## 🛠️ Troubleshooting

**`GEMINI_API_KEY not found` error:**
- Make sure `.env` file exists in the project root
- Make sure the key name is exactly `GEMINI_API_KEY`

**`ModuleNotFoundError`:**
- Make sure your venv is activated: `source venv/bin/activate`
- Run `pip install -r requirements.txt` again

**Streamlit Cloud deployment failing:**
- Check that you added the secret key in the Streamlit dashboard
- Check the **Logs** tab in your Streamlit Cloud app for error details

---

## 📄 License

MIT License — feel free to use and modify.

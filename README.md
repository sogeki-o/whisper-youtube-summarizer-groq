🎥 Whisper + YouTube + URL Summarizer (Groq + LangChain)

whisper-youtube-summarizer-groq is a Streamlit-based application that can summarize YouTube videos (via Whisper speech-to-text) or any website URL using LangChain and Groq Llama-3 LLMs.

It downloads YouTube audio using yt-dlp, transcribes it using Whisper, splits the text into chunks, summarizes each chunk (Map step), and finally merges everything into a polished summary (Reduce step).

🚀 Features
🎬 YouTube Summarization (Audio → Text → Summary)

Uses yt-dlp to download video audio

Converts audio → text using Whisper (tiny model by default)

Works even when YouTube disables transcripts

High accuracy for long videos

🌐 Website Summarization

Extracts readable text using UnstructuredURLLoader

Handles long articles, blogs, documentation, essays, etc.

🧠 LLM Summarization Using Groq

Powered by Llama-3.1-8B-Instant

Extremely fast response time due to Groq inference engine

Map–Reduce summarization pipeline:

🔹 Map: summarize each chunk

🔹 Reduce: combine all summaries into final result

📦 Project Structure
whisper-youtube-summarizer-groq/
│
├── app.py                 # Main Streamlit application
├── requirements.txt       # Dependencies
├── .env.example           # Template for environment variable
├── .gitignore
└── downloads/             # Auto-created for audio files

🔧 Installation & Setup
1️⃣ Clone the Repository
git clone https://github.com/Shehjad2019/whisper-youtube-summarizer-groq.git
cd whisper-youtube-summarizer-groq

2️⃣ Create Virtual Environment
python -m venv venv
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows

3️⃣ Install Dependencies
pip install -r requirements.txt


If Whisper requires PyTorch, install CPU version:

pip install torch --index-url https://download.pytorch.org/whl/cpu

4️⃣ Setup Environment File

Copy:

cp .env.example .env


Then edit .env:

GROQ_API_KEY=your_groq_api_key_here

▶️ Running the App

Start Streamlit:

streamlit run app.py


Then paste:

a YouTube URL

or any valid website URL

Click Summarize Content.

🔍 How It Works Internally
🎥 YouTube Flow

yt-dlp downloads audio

Whisper converts audio → text

Text is wrapped in a LangChain Document

Chunked using RecursiveCharacterTextSplitter

Map-Reduce summarization runs on Groq Llama-3

🌐 Website Flow

Loads text using UnstructuredURLLoader

Splits into chunks

Summarizes using same Map-Reduce pipeline

🧠 Map–Reduce Summarization (LangChain)

Map Prompt: summarize each chunk

Reduce Prompt: merge summaries into final output

Handles very large inputs efficiently

🔑 Environment Variables
GROQ_API_KEY=your_groq_key_here

👤 Author

Shehjad Patel
GitHub: https://github.com/Shehjad2019

⭐ Like this project?

If this helped you, please star the repo ⭐ on GitHub:

👉 https://github.com/Shehjad2019/whisper-youtube-summarizer-groq
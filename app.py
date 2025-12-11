import os
import validators
import streamlit as st
import yt_dlp
import whisper

from langchain_groq import ChatGroq
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import UnstructuredURLLoader
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate


# ==============================
# STREAMLIT UI
# ==============================

st.set_page_config(page_title="URL / YouTube Summarizer", page_icon="🦜")
st.title("🦜 LangChain: Summarize Text From URL or YouTube")
st.subheader("Paste any website link or YouTube URL below")


# ---------------- Sidebar – API Key ---------------- #

with st.sidebar:
    groq_api_key = st.text_input("Groq API Key", type="password")


generic_url = st.text_input("Enter Website or YouTube URL", label_visibility="collapsed")


# ==============================
# LOAD LLM (Groq)
# ==============================

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    groq_api_key=groq_api_key
)


# ==============================
# PROMPTS FOR MAP–REDUCE
# ==============================

map_prompt = ChatPromptTemplate.from_template("""
Summarize the content chunk below clearly and concisely.

Content:
{text}

Summary:
""")

reduce_prompt = ChatPromptTemplate.from_template("""
Combine the following partial summaries into a single meaningful summary.
Keep it short, clear, and include important points.

Partial Summaries:
{text}

Final Summary:
""")

map_chain = map_prompt | llm
reduce_chain = reduce_prompt | llm


# ==============================
# FUNCTION – YOUTUBE AUDIO → TEXT VIA WHISPER
# ==============================

def load_youtube_transcript(url, save_dir="downloads"):
    os.makedirs(save_dir, exist_ok=True)
    audio_path = os.path.join(save_dir, "audio.mp3")

    # Download audio using yt-dlp
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": audio_path,
        "quiet": True,
        "no_warnings": True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    # Transcribe using Whisper
    model = whisper.load_model("tiny")   # can switch to "base", "tiny", etc.
    result = model.transcribe(audio_path)

    text = result["text"]

    # Return as LangChain Document
    return [Document(page_content=text)]


# ==============================
# MAIN BUTTON
# ==============================

if st.button("Summarize Content"):

    if not groq_api_key.strip():
        st.error("Please enter your Groq API Key.")
    elif not generic_url.strip():
        st.error("Please provide a URL.")
    elif not validators.url(generic_url):
        st.error("Invalid URL format.")
    else:
        try:
            with st.spinner("Processing... Please wait ⏳"):

                # ------------- HANDLE YOUTUBE LINKS ---------------- #
                if "youtube.com" in generic_url or "youtu.be" in generic_url:
                    docs = load_youtube_transcript(generic_url)

                # ------------- HANDLE NORMAL WEBSITES ---------------- #
                else:
                    loader = UnstructuredURLLoader(
                        urls=[generic_url],
                        ssl_verify=False,
                        headers={"User-Agent": "Mozilla/5.0"}
                    )
                    docs = loader.load()

                # ------------- CHUNK INTO PIECES ---------------- #
                splitter = RecursiveCharacterTextSplitter(
                    chunk_size=1500,
                    chunk_overlap=200
                )
                chunks = splitter.split_documents(docs)

                # ------------- MAP STEP ---------------- #
                map_summaries = []
                for chunk in chunks:
                    resp = map_chain.invoke({"text": chunk.page_content})
                    map_summaries.append(resp.content)

                # ------------- REDUCE STEP ---------------- #
                final_output = reduce_chain.invoke({
                    "text": "\n\n".join(map_summaries)
                })

                st.success(final_output.content)

        except Exception as e:
            st.exception(f"Exception: {e}")

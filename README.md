# 🎥 Video Agent — AI-Powered Video Intelligence & RAG

An AI-powered video analysis system that transforms long-form video/audio content into **structured insights, searchable knowledge, and context-aware Q&A**.

Instead of manually watching an entire video, Video Agent processes the content through an AI pipeline to generate a concise summary, identify action items and decisions, extract open questions, and allow users to interact with the transcript using **Retrieval-Augmented Generation (RAG)**.

> **From raw video → transcription → structured intelligence → semantic search → grounded Q&A**

---

## 🚀 Features

### 🎙️ Intelligent Transcription

* Extracts audio from YouTube videos or uploaded media.
* Uses **OpenAI Whisper** for English transcription.
* Supports **Hinglish/multilingual transcription** through Sarvam AI.
* Automatically processes audio into manageable chunks.

### 🧠 AI-Powered Video Analysis

The system extracts structured information from the transcript:

* 📌 **Automatic Title Generation**
* 📝 **Meeting/Video Summary**
* ✅ **Action Items**
* 🎯 **Key Decisions**
* ❓ **Open Questions**
* 💬 **Interactive Q&A**

### 🔎 Retrieval-Augmented Generation

The transcript is converted into searchable vector representations and stored in a vector database.

When the user asks a question:

```text
User Question
      ↓
Semantic Retrieval
      ↓
Relevant Transcript Chunks
      ↓
LLM Context Injection
      ↓
Grounded Answer
```

The system is designed to answer questions **using the available video context rather than relying purely on the model's general knowledge.**

### 🌐 YouTube Support

Paste a YouTube URL and the application automatically:

```text
YouTube URL
    ↓
Audio Extraction
    ↓
Audio Processing
    ↓
Whisper / Sarvam Transcription
    ↓
Transcript
    ↓
AI Analysis
    ↓
Vector Database
    ↓
RAG Q&A
```

### 🖥️ Streamlit Interface

The project includes a Streamlit interface for:

* Video input
* Processing status
* Transcript viewing
* AI-generated insights
* Interactive Q&A
* Pipeline progress tracking

---

# 🏗️ System Architecture

```text
                         ┌─────────────────────┐
                         │   YouTube / Audio    │
                         │        Input         │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │   Audio Extraction  │
                         │      yt-dlp/FFmpeg   │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │   Audio Chunking    │
                         └──────────┬──────────┘
                                    │
                       ┌────────────┴────────────┐
                       │                         │
                       ▼                         ▼
                ┌─────────────┐           ┌─────────────┐
                │   Whisper   │           │  Sarvam AI  │
                │   English   │           │  Hinglish   │
                └──────┬──────┘           └──────┬──────┘
                       │                         │
                       └────────────┬────────────┘
                                    ▼
                         ┌─────────────────────┐
                         │     Transcript      │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │   LLM Analysis      │
                         │                     │
                         │ • Title             │
                         │ • Summary           │
                         │ • Action Items      │
                         │ • Decisions         │
                         │ • Questions         │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │    Vector Store     │
                         │                     │
                         │ Embeddings + Search │
                         └──────────┬──────────┘
                                    │
                              User Question
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │ Semantic Retrieval  │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │       LLM           │
                         │ Context + Question  │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │  Grounded Answer    │
                         └─────────────────────┘
```

---

# 🛠️ Tech Stack

| Layer                  | Technology                     |
| ---------------------- | ------------------------------ |
| UI                     | Streamlit                      |
| Programming Language   | Python                         |
| Video/Audio            | yt-dlp                         |
| Media Processing       | FFmpeg                         |
| Speech-to-Text         | OpenAI Whisper                 |
| Multilingual STT       | Sarvam AI                      |
| LLM                    | Mistral AI                     |
| AI Framework           | LangChain                      |
| RAG                    | Retrieval-Augmented Generation |
| Vector Database        | Chroma / Qdrant                |
| Embeddings             | Sentence Transformers          |
| Environment Management | python-dotenv                  |

---

# 📁 Project Structure

```text
VIDEO_AGENT/
│
├── app.py
├── requirements.txt
├── .env.example
├── .gitignore
│
├── core/
│   ├── __init__.py
│   ├── transcriber.py
│   ├── summarizer.py
│   ├── extractor.py
│   ├── rag_engine.py
│   └── vector_store.py
│
├── data/
│   └── ...
│
└── README.md
```

> API keys and environment-specific configuration are intentionally excluded from the repository.

---

# ⚙️ How It Works

## 1. Input Processing

The user provides either:

* YouTube URL
* Audio/video file

For YouTube URLs, `yt-dlp` is used to retrieve the audio and FFmpeg handles media processing.

---

## 2. Speech-to-Text

The extracted audio is divided into manageable chunks.

For English:

```text
Audio → Whisper → Transcript
```

For Hinglish/multilingual input:

```text
Audio → Sarvam AI → Transcript
```

This allows the system to support different transcription workflows depending on the selected language.

---

## 3. Transcript Analysis

The generated transcript is passed to the LLM for structured analysis.

The system extracts:

```text
Title
Summary
Action Items
Key Decisions
Open Questions
```

This transforms an unstructured transcript into information that can be quickly consumed.

---

## 4. Vectorization

The transcript is split into smaller semantic chunks.

Each chunk is converted into an embedding and stored in the vector database.

```text
Transcript
    ↓
Chunking
    ↓
Embeddings
    ↓
Vector Database
```

---

## 5. RAG-Based Q&A

When a user asks a question, the system performs semantic retrieval.

For example:

```text
Question:
"What deadline was discussed for the project?"
```

The retriever searches the transcript for the most relevant sections.

The retrieved context is then passed to the LLM:

```text
Question + Retrieved Context
            ↓
           LLM
            ↓
     Contextual Answer
```

This helps keep answers grounded in the source material.

---

# 💡 Example Use Cases

### 🎓 Educational Videos

Ask questions about a long technical lecture without watching the entire video.

### 💼 Meetings

Automatically identify:

* Decisions
* Responsibilities
* Deadlines
* Follow-up questions

### 📺 YouTube Research

Convert long interviews, podcasts, tutorials, and discussions into searchable knowledge.

### 🧑‍💻 Technical Learning

Ask questions directly against programming tutorials, conference talks, and technical lectures.

### 🏢 Knowledge Management

Transform recorded discussions into structured and searchable organizational knowledge.

---

# 🔐 Environment Variables

Create a `.env` file locally:

```env
MISTRAL_API_KEY=your_mistral_api_key
SARVAM_API_KEY=your_sarvam_api_key

LANGCHAIN_API_KEY=your_langsmith_api_key
LANGCHAIN_TRACING_V2=true
LANGCHAIN_PROJECT=video-agent

WHISPER_MODEL=small
SARVAM_STT_MODEL=saaras:v2.5
```

**Never commit `.env` to GitHub.**

The repository includes `.env.example` so other developers know which variables are required.

---

# 🚀 Installation

## 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/VIDEO_AGENT.git

cd VIDEO_AGENT
```

## 2. Create a Virtual Environment

### Windows

```powershell
python -m venv myvirt

myvirt\Scripts\activate
```

### macOS/Linux

```bash
python3 -m venv myvirt

source myvirt/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Configure Environment Variables

Create:

```text
.env
```

and add your API keys.

---

## 5. Install FFmpeg

FFmpeg must be available on your system for audio/video processing.

Verify:

```bash
ffmpeg -version
```

---

## 6. Run the Application

```bash
streamlit run app.py
```

The application will be available locally through Streamlit.

---

# 📊 AI Pipeline

The complete processing pipeline is:

```text
INPUT
  │
  ▼
YouTube / Audio / Video
  │
  ▼
Audio Extraction
  │
  ▼
Chunking
  │
  ▼
Speech Recognition
  │
  ├── Whisper
  │
  └── Sarvam AI
  │
  ▼
Transcript
  │
  ▼
LLM Analysis
  │
  ├── Title
  ├── Summary
  ├── Action Items
  ├── Key Decisions
  └── Open Questions
  │
  ▼
Text Chunking
  │
  ▼
Embeddings
  │
  ▼
Vector Database
  │
  ▼
Retriever
  │
  ▼
Relevant Context
  │
  ▼
LLM
  │
  ▼
Grounded Q&A
```

---

# ⚡ Engineering Considerations

The project is designed around a modular AI pipeline so individual components can be replaced independently.

For example:

```text
Whisper
   ↓
Alternative STT Provider
```

or:

```text
Mistral
   ↓
Another LLM Provider
```

without fundamentally changing the RAG architecture.

The analysis pipeline also aims to minimize unnecessary LLM calls by combining related extraction tasks into a structured analysis step.

---

# 🔭 Future Improvements

Planned improvements include:

* [ ] Faster transcription pipeline
* [ ] Streaming AI responses
* [ ] Persistent vector database
* [ ] Video timestamp-aware answers
* [ ] Citation of transcript segments
* [ ] Speaker diarization
* [ ] Better multilingual support
* [ ] Background processing for long videos
* [ ] Caching of processed videos
* [ ] Async processing
* [ ] Production deployment
* [ ] Authentication and user sessions
* [ ] Observability with LangSmith
* [ ] Evaluation pipeline for RAG quality
* [ ] Dockerization

---

# 🧪 Future Production Architecture

The application can be extended into a scalable architecture:

```text
                 Client
                   │
                   ▼
              Streamlit/UI
                   │
                   ▼
              FastAPI API
                   │
          ┌────────┴────────┐
          │                 │
          ▼                 ▼
      Job Queue         Metadata DB
          │
          ▼
   Background Worker
          │
    ┌─────┴─────┐
    │           │
    ▼           ▼
   STT        LLM Analysis
    │           │
    └─────┬─────┘
          ▼
     Vector Store
          │
          ▼
       RAG API
          │
          ▼
        Client
```

This architecture would allow the system to handle longer videos and multiple users more efficiently.

---

# 🎯 What This Project Demonstrates

This project demonstrates practical experience with:

* Generative AI application development
* Large Language Models
* LangChain
* Retrieval-Augmented Generation
* Vector databases
* Semantic search
* Embeddings
* Speech-to-text systems
* Multilingual AI
* Prompt engineering
* Structured information extraction
* AI pipeline design
* API integration
* Streamlit application development
* Environment and secret management

---

# 👨‍💻 Author

**Aditya Kumar Prasad**

CSE Graduate | AI/ML Engineer | Generative AI Developer

Focused on building practical AI systems using:

```text
Python
Machine Learning
Deep Learning
LLMs
RAG
LangChain
LangGraph
MCP
Generative AI
```

---

## ⭐ If You Find This Project Interesting

Consider giving the repository a ⭐ and exploring the implementation.

**Built to explore how unstructured video content can be transformed into searchable, actionable knowledge using modern AI systems.**

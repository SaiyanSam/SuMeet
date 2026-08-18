# SuMeet

> **An Agentic AI Meeting Intelligence Assistant for Transcription, Structured Information Extraction, and Meeting Analytics**

## Overview

SuMeet is an end-to-end **agentic meeting intelligence system** that transforms meeting audio or transcripts into structured, searchable, and actionable information.

Rather than relying on a single LLM prompt, SuMeet follows a **hybrid AI architecture** where an intelligent agent routes user requests to specialized tools while deterministic components handle data processing, validation, retrieval, analytics, and visualization.

The long-term objective is to build a reliable meeting assistant capable of:

* Transcribing meeting audio into timestamped transcripts
* Generating hierarchical meeting summaries
* Extracting action items, decisions, and blockers
* Preserving evidence and timestamps for every extracted item
* Supporting semantic transcript search
* Performing meeting analytics using structured DataFrames
* Creating visualizations from validated meeting data
* Exporting structured meeting minutes in multiple formats

The project is designed as a placement-ready demonstration of modern **Agentic AI**, **LLM Engineering**, and **NLP System Design**.

---

# Project Architecture

```text
Audio / Transcript
        │
        ▼
Transcript Processing
        │
        ▼
Structured Meeting Record
        │
        ▼
Meeting Agent
        │
 ┌──────┼───────────────┐
 ▼      ▼               ▼
Summary  Actions    Transcript Search
Tool     Tool            Tool
 │        │               │
 └────────┼───────────────┘
          ▼
 Meeting Analytics
          ▼
 Visualizations & Export
```

---

# Technology Stack

* Python
* Pydantic
* LangChain
* LangChain Expression Language (LCEL)
* Whisper (faster-whisper)
* Sentence Transformers
* FAISS
* Streamlit
* Pandas
* Matplotlib
* spaCy
* SQLite (planned)

---

## In Progress

* None

## Next Milestone

Implement the audio transcription pipeline using **faster-whisper** so both transcript and audio inputs produce the same validated meeting representation.

---

# Long-Term Vision

The first release focuses on a **single-meeting intelligence assistant**.

Future versions will extend the system into a **persistent meeting knowledge platform** capable of:

* Cross-meeting search
* Meeting history
* Multi-meeting analytics
* SQL-powered querying
* Calendar integration
* RAG over previous meetings
* Workflow automation
* Multi-language support


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

# Development Roadmap

| Day        | Objective                                                                                                | Deliverable                              | Progress  |
| ---------- | -------------------------------------------------------------------------------------------------------- | ---------------------------------------- | --------- |
| **Day 1**  | Repository foundation, transcript parsing, validation pipeline, Pydantic models, JSON export, unit tests | Transcript → Validated JSON pipeline     | ✅ Done    |
| **Day 2**  | Audio ingestion and Whisper transcription                                                                | Audio → Timestamped transcript           | ⏳ Planned |
| **Day 3**  | LCEL chains and structured extraction                                                                    | Chunk summaries, action items, decisions | ⏳ Planned |
| **Day 4**  | Agent framework and tool registry                                                                        | Tool selection and validated execution   | ⏳ Planned |
| **Day 5**  | Semantic search and retrieval                                                                            | FAISS-powered transcript search          | ⏳ Planned |
| **Day 6**  | Meeting analytics and visualization                                                                      | DataFrames, metrics, charts              | ⏳ Planned |
| **Day 7**  | Streamlit interface and exports                                                                          | Complete working application             | ⏳ Planned |
| **Day 8**  | Evaluation framework                                                                                     | Annotated dataset and evaluation metrics | ⏳ Planned |
| **Day 9**  | Documentation and GitHub polish                                                                          | Architecture, demo GIF, screenshots      | ⏳ Planned |
| **Day 10** | Final optimization and resume-ready release                                                              | Stable v1.0 release                      | ⏳ Planned |

---

# Current Status

## Completed

* Repository initialized
* Conda environment configured
* Project structure created
* Transcript parser
* Transcript cleaner
* Timestamp parsing
* Speaker parsing
* Pydantic transcript models
* Pydantic meeting models
* Tool-call schemas
* JSON export pipeline
* Unit tests (**29 passing**)

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

---

# Repository Status

**Current Version:** Day 1 Complete

**Test Status:** ✅ 29 Passing

**Development Stage:** Active


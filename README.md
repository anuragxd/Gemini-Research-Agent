# 🤖 Structured Researcher Agent

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-UI-red)
![LangGraph](https://img.shields.io/badge/LangGraph-Orchestration-orange)
![Gemini](https://img.shields.io/badge/Gemini-1.5%20Flash-green)

A beginner-friendly AI agent built with **LangGraph**, **Streamlit**, and **Google Gemini**. This application takes a user-provided topic, performs live web research, and autonomously writes a polished blog post about it.

It demonstrates a **Sequential Pipeline** architecture where data flows deterministically through specialized AI workers.

## 🌟 Features

* **Multi-Step Workflow:** Separates logic into distinct "Researcher" and "Writer" nodes.
* **Live Web Access:** Uses `DuckDuckGo` to fetch real-time information (no API key required for search).
* **State Management:** Utilizes LangGraph's `TypedDict` to pass context between steps.
* **Interactive UI:** A clean Streamlit interface that visualizes the "Thinking" process and final output side-by-side.

## 🛠️ Architecture

The agent follows a linear graph structure:

1.  **Start:** User inputs a topic (e.g., "The future of Quantum Computing").
2.  **Node 1 (Researcher):** * Executes a web search.
    * Summarizes raw results into key bullet points using **Gemini 1.5 Flash**.
3.  **Node 2 (Writer):** * Receives the research notes.
    * Drafts a formatted blog post based *strictly* on those notes.
4.  **End:** Displays the final result in the UI.

## 🚀 Getting Started

### Prerequisites
* Python 3.9 or higher
* A [Google Gemini API Key](https://aistudio.google.com/) (Free tier is sufficient)

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd researcher_agent

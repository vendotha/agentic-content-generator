# 🤖 Agentic Blog Generator

**An autonomous ReAct agent that researches a topic in real time and writes a publication-ready blog post — powered by Google Gemini and LangChain.**

Give it a topic, and the agent reasons about what it needs to know, searches the web and Wikipedia to fill in the gaps, and synthesizes everything into a structured Markdown article — with no human in the loop after the initial prompt.

<p>
  <img alt="Python" src="https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white">
  <img alt="LangChain" src="https://img.shields.io/badge/LangChain-Agents-1C3C3C?logo=langchain&logoColor=white">
  <img alt="Gemini" src="https://img.shields.io/badge/Gemini-2.5%20Flash-8E75B2?logo=googlegemini&logoColor=white">
</p>

---

## ✨ Overview

Most "AI writer" scripts are a single prompt-and-response call to an LLM — the model writes from what it already knows, which means it can hallucinate facts and go stale immediately after training. This project is different: it's built as an **agent**, not a chatbot. Given a topic, it autonomously decides *what to look up*, *when to look it up*, and *when it has enough information to write* — using the classic **ReAct (Reasoning + Acting)** loop:

```
Thought → Action → Observation → Thought → ... → Final Answer
```

At each step the agent reasons about what it still needs, picks a tool, reads the result, and repeats — fully visible in the console via live trace output — until it's confident enough to write the final post.

## 🧠 Key Features

- **Autonomous research loop** — the agent, not a hardcoded pipeline, decides which tool to call and when, based on its own reasoning about what the topic still needs.
- **Multi-tool grounding** — combines **DuckDuckGo Search** (current, broad web results) with **Wikipedia** (structured background/reference facts) so the model isn't writing from memory alone.
- **Custom prompt engineering** — the standard LangChain ReAct prompt is extended with a hand-written instruction set that constrains the agent's final output to a consistent structure (Title → Introduction → Content → Summary), turning a general-purpose reasoning prompt into a reliable content-generation pipeline.
- **Transparent reasoning trace** — runs with `verbose=True` so every Thought/Action/Observation step is visible, making the agent's decision process auditable rather than a black box.
- **Zero-touch output** — writes the final Markdown post straight to `blog_output.md`, ready to publish or drop into a static site generator.

## 🏗️ Architecture

```
                 ┌─────────────────────┐
   User Topic ──▶│   ReAct Agent Loop   │
                 │  (Gemini 2.5 Flash)  │
                 └──────────┬───────────┘
                             │  Thought → Action
              ┌──────────────┴──────────────┐
              ▼                             ▼
     ┌─────────────────┐          ┌──────────────────┐
     │ DuckDuckGo Search │          │  Wikipedia Query  │
     │   (live web)       │          │  (reference facts) │
     └──────────┬────────┘          └─────────┬────────┘
                 │          Observation        │
                 └──────────────┬──────────────┘
                                 ▼
                     Repeats until agent has
                      enough grounded info
                                 │
                                 ▼
                  Final Answer → blog_output.md
```

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **LLM** | Google Gemini 2.5 Flash (`langchain-google-genai`) |
| **Agent framework** | LangChain (`create_react_agent` + `AgentExecutor`) |
| **Agent prompt** | LangChain Hub — `hwchase17/react`, extended with custom output-formatting instructions |
| **Research tools** | DuckDuckGo Search (`duckduckgo_search` / `ddgs`), Wikipedia API (`wikipedia`) |
| **Config/secrets** | `python-dotenv` |
| **Language** | Python 3.10+ |

## ⚙️ Installation

1.  **Clone the repository** (or download and unzip the folder).

2.  **Create a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install the required packages:**
    (Versions are pinned — the LangChain/Gemini ecosystem moves fast, and untested version combinations can silently break agent construction.)
    ```bash
    pip install -r requirements.txt
    ```

## 🔑 Configuration

This project requires a Google (Gemini) API key.

1.  Get a free key from [Google AI Studio](https://aistudio.google.com/app/apikey).
2.  Create a file named `.env` in the project root.
3.  Add your key:

    ```ini
    GOOGLE_API_KEY="AIzaSy...YourSecretKeyGoesHere"
    ```

`.env` is already listed in `.gitignore`, so your key won't be committed.

## 🚀 Usage

Run the script from your terminal:

```bash
python blog_generator_gemini.py
```

You'll be prompted for a topic:

```
Enter the blog topic: The AI revolution in finance
```

The agent then researches live (its Thought/Action/Observation steps print to the console as it works), writes the final post, prints it, and saves it to `blog_output.md` in the project root — overwriting any previous run.

**Sample output structure:**

```markdown
# The AI Revolution in Finance: How Artificial Intelligence is Reshaping Financial Services

## Introduction
...

## Content
...

## Summary
...
```

## 📁 Project Structure

```
.
├── blog_generator_gemini.py   # Agent construction, ReAct prompt, and CLI entry point
├── requirements.txt           # Pinned dependencies
├── blog_output.md             # Overwritten each run with the latest generated post
└── .env                       # Your GOOGLE_API_KEY (not committed)
```

## 🎯 Skills Demonstrated

- Designing and prompting an **autonomous agent** (ReAct pattern) rather than a single-shot LLM call
- **Tool use / function calling** integration — wiring external tools (search, Wikipedia) into an LLM's reasoning loop
- **Prompt engineering** — extending a general-purpose agent prompt to reliably constrain output format
- Working with the **LangChain** ecosystem (agents, prompts, tool wrappers, LangChain Hub) and the **Gemini API**
- Dependency and environment management in a fast-moving library ecosystem (pinned requirements, deliberate use of a stable agent API over a newer one that had compatibility issues)

## 🧩 Known Issues / Notes

- **Gemini API overload:** occasionally returns a `503 The model is overloaded` error — a temporary capacity issue on Google's side; simply re-run.
- **API used deliberately:** uses `create_react_agent` rather than the newer `create_tool_calling_agent`, which hit compatibility issues with the available Gemini libraries — a conscious tradeoff for stability over using the latest API.
- **Search depth:** DuckDuckGo results are short snippets, not full page content, which can limit research depth on very niche topics.

## 🗺️ Roadmap

- [ ] Migrate from `AgentExecutor` to **LangGraph** for a more modern, extensible agent architecture
- [ ] Add a tool that scrapes full page content (via BeautifulSoup) instead of relying on search snippets alone
- [ ] Human-in-the-loop mode: generate an outline first, get approval, then write the full post

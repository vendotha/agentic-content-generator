# Agent-Based Blog Generation System

This project is a Python-based system that uses the Google Gemini LLM and LangChain to automatically generate high-quality blog posts on any given topic.

The system is built as a ReAct (Reasoning and Acting) agent that can use tools—specifically DuckDuckGo Search and Wikipedia—to conduct research before writing.

## ⚙️ Installation

1.  **Clone the repository** (or download and unzip the folder).

2.  **Create a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install the required packages:**
    (These versions are pinned for stability.)
    ```bash
    pip install -r requirements.txt
    ```

## Configuration

This project requires a Google (Gemini) API key.

1.  Get your key from [Google AI Studio](https://aistudio.google.com/app/apikey).
2.  Create a file named `.env` in the root of the project.
3.  Add your API key to this file:

    ```ini
    GOOGLE_API_KEY="AIzaSy...YourSecretKeyGoesHere"
    ```

## 🚀 How to Run

Run the script from your terminal:

```bash
python blog_generator_gemini.py
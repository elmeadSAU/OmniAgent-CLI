# 🤖 OmniAgent-CLI

An autonomous, multi-tool terminal AI Agent built with the official Google GenAI SDK. OmniAgent-CLI implements a localized reasoning loop capable of running terminal 
commands, self-correcting script execution failures, scraping information from the web, and profiling dataset contents.

## 🛠️ Integrated Tool Architecture
* **Self-Correcting Shell Engine:** Executes bash processes and catches system `stderr` tracebacks to dynamically patch and retry broken python execution parameters.
* **Web Search Extractor:** Automatically fetches search snippets to bring real-time data or updated library code documentation into the workspace context.
* **Data Profiler:** Reads local tabular data formats (CSV/Excel) to instantly profile column layouts and identify missing metrics for structured calculations.

## 🚀 Quickstart Guide

### 1. Environment Installation
Ensure your dependencies are configured from the project folder root:
```bash
pip install -r requirements.txt

Set your personal Gemini API key variable:
export GEMINI_API_KEY="your_api_key_here"


### 2. Execution Run
python3 agent.py "Inspect test_metrics.csv, check for missing parameters, and run a python script that fills missing numeric parameters with the average score of the 
column."

---

## 🗺️ Future Roadmap

Track upcoming features and architectural expansions planned for the core framework:

- [ ] **Local Vector Storage Integration (RAG)**: Implement localized vector indexing to allow the agent to reference historical local execution context.
- [ ] **Automated Dependency Management**: Enable the shell engine to dynamically identify missing packages from stderr tracebacks and execute pip install 
automatically.
- [ ] **Web Interface Dashboard**: Build a lightweight web UI to monitor the agent's multi-tool execution chains in real-time.

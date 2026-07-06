import os
import sys
import time
import re
import subprocess
import requests
import pandas as pd
from google import genai
from google.genai import types
from google.genai.errors import ClientError

client = genai.Client()

def execute_terminal_command(command: str) -> str:
    """Executes a shell command locally and returns output."""
    print(f"\n⚙️ [Tool: Terminal] Executing: {command}")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=30)
        return f"STDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"
    except Exception as e:
        return f"Execution Failed: {str(e)}"

def search_and_scrape_web(query: str) -> str:
    """Searches the web and extracts text snippets safely."""
    print(f"\n🌐 [Tool: Web Search] Searching for: '{query}'")
    try:
        url = f"https://html.duckduckgo.com/html/?q={requests.utils.quote(query)}"
        headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"}
        response = requests.get(url, headers=headers, timeout=15)
        
        if response.status_code == 200:
            snippets = []
            matches = re.findall(r'class="result__snippet".*?>(.*?)</a>', response.text, re.DOTALL)
            for match in matches[:4]:
                clean_text = re.sub(r'<.*?>', '', match)
                snippets.append(clean_text.strip())
            return "\n\n".join(snippets) if snippets else "No snippets found."
        return f"Search failed (Status {response.status_code})"
    except Exception as e:
        return f"Search Error: {str(e)}"

def inspect_and_profile_dataset(file_path: str) -> str:
    """
    Reads local CSV/Excel datasets to profile missing values, columns, data shapes, 
    and data summaries. Use this to find schema bugs or plan visualization runs.
    """
    print(f"\n📊 [Tool: Data Profiler] Inspecting: '{file_path}'")
    try:
        if not os.path.exists(file_path):
            return f"Data Error: File '{file_path}' not found in local workspace."
        
        # Auto-detect structure
        df = pd.read_csv(file_path) if file_path.endswith('.csv') else pd.read_excel(file_path)
        
        summary = {
            "shape": df.shape,
            "columns": list(df.columns),
            "missing_values": df.isnull().sum().to_dict(),
            "head_preview": df.head(2).to_dict(orient='records')
        }
        return f"Dataset Profile successfully extracted:\n{str(summary)}"
    except Exception as e:
        return f"Data Profiling Failure: {str(e)}"

def run_agent_loop(user_goal: str):
    print("============================================================")
    print("🤖 OmniAgent-CLI: Complete Multi-Agent Suite Engaged")
    print("============================================================")
    
    available_tools = {
        "execute_terminal_command": execute_terminal_command,
        "search_and_scrape_web": search_and_scrape_web,
        "inspect_and_profile_dataset": inspect_and_profile_dataset
    }
    
    config = types.GenerateContentConfig(
        system_instruction=(
            """You are a multi-tool Data Science and Shell Execution Agent. 
You can parse files, run shell workflows, search the web, and correct your own failures.
If tasked with data updates, use 'inspect_and_profile_dataset' first to view its columns,
then execute a python fix script to output data visualizations or metrics perfectly."""
        ),
        tools=[execute_terminal_command, search_and_scrape_web, inspect_and_profile_dataset],
        temperature=0.1
    )
    
    chat = client.chats.create(model="gemini-2.5-flash", config=config)
    current_prompt = user_goal
    
    while True:
        try:
            time.sleep(2.5)
            response = chat.send_message(current_prompt)
            
            if response.function_calls:
                for call in response.function_calls:
                    tool_name = call.name
                    tool_args = call.args
                    
                    if tool_name in available_tools:
                        tool_output = available_tools[tool_name](**tool_args)
                        current_prompt = tool_output
                    else:
                        current_prompt = f"Error: Tool '{tool_name}' not found."
            else:
                print("\n🏁 [Agent Analysis Summary]:")
                print(response.text)
                break
                
        except ClientError as e:
            if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                print("\n⚠️ Quota Limit. Cooling down for 30 seconds...")
                time.sleep(30)
                continue
            else:
                print(f"\n❌ Client Error: {e}")
                break
        except Exception as e:
            print(f"\n❌ Unexpected Loop Error: {e}")
            break

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 agent.py 'Your execution goal'")
        sys.exit(1)
    run_agent_loop(sys.argv[1])

# imports

import os
import io
import sys
from dotenv import load_dotenv
from openai import OpenAI
import gradio as gr
import subprocess
from IPython.display import Markdown, display
from prompts import build_messages
import ast
import time



load_dotenv(override=True)
openrouter_api_key = os.getenv('OPENROUTER_API_KEY')
openai_api_key = os.getenv('OPENAI_API_KEY')


if openrouter_api_key:
    # Print the first few characters of the key for verification purposes
    print(f"OpenRouter API Key exists and begins {openrouter_api_key[:6]}")

# Connect to client libraries
openai = OpenAI()
openrouter_url = "https://openrouter.ai/api/v1"
openrouter = OpenAI(api_key=openrouter_api_key, base_url=openrouter_url)
MODELS = {
    "Qwen 3.8 Flash": "qwen/qwen3.8-flash",
    "GPT-5.6 Luna": "openai/gpt-5.6-luna",
    "Gemini 3.5 Flash Lite": "google/gemini-3.5-flash-lite",
    "Gemini 3.8 Flash": "google/gemini-3.8-flash",
    "Grok 4.3": "x-ai/grok-4.3",
    "Claude Sonnet 5": "anthropic/claude-sonnet-5",
}

PRICES = {
    "Qwen 3.8 Flash": (0.15, 0.47),
    "GPT-5.6 Luna": (0.20, 1.20),
    "Gemini 3.5 Flash Lite": (0.30, 2.50),
    "Gemini 3.8 Flash": (0.75, 3.75),
    "Grok 4.3": (1.25, 2.50),
    "Claude Sonnet 5": (3.00, 15.00),
}


def clean_output(text): #Removes any markdown from LLM response if any
    """Remove markdown code block wrappers from an LLM text response.

    Args:
        text (str): The raw text response from the language model.

    Returns:
        str: The cleaned text with markdown code fences removed if present.
    """
    # Remove leading and trailing whitespace
    text = text.strip()
    # Check if the response is wrapped in markdown code blocks
    if text.startswith("```"):
        lines = text.split("\n")
        # Strip the opening code fence line
        lines = lines[1:]
        # Strip the closing code fence line if present
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        text = "\n".join(lines)
    return text


def strip_docstrings(tree): #Inputs tree from ast.parse(code)
    for node in ast.walk(tree): #ast.walk loops every node
        if isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)): #Only loops nodes with possibility of docstrings
            if (node.body #Checks that there is something inside node, if not would crash 
                    and isinstance(node.body[0], ast.Expr) #ast.Expr means a value sitting on its own line not assigned to anything (exactly what a doc string is)
                    and isinstance(node.body[0].value, ast.Constant)
                    and isinstance(node.body[0].value.value, str)):
                node.body = node.body[1:] #If it is a docstring then it is cut off returning just the code
    return tree


def check_logic(original, documented):
    try:
        original_tree = ast.parse(original)
        documented_tree = ast.parse(documented)
    except SyntaxError:
        return "⚠ Couldn't check: the code isn't valid Python"
    stripped_original = strip_docstrings(original_tree)
    stripped_documented = strip_docstrings(documented_tree)
    dump_original = ast.dump(stripped_original)
    dump_documented = ast.dump(stripped_documented)
    if dump_original == dump_documented:
        return "Logic Identical"
    else:
        return "Logic has changed beware"
    

def generate(code, model_name):
    """Generate documentation for the provided code using the OpenRouter API.

    Args:
        code (str): The source code to be documented.
        model name

    Returns:
        tuple[str, str, str]: The documented code, the path to the saved
        file, and the logic check result.
    """
    # Request a completion from the OpenRouter API using the configured model and prompt builder
    start = time.perf_counter()
    stream = openrouter.chat.completions.create(
        model=MODELS[model_name],
        messages=build_messages(code),
        temperature=0,
        stream=True,
        stream_options={"include_usage": True},
    )
    reply = ""
    usage = None
    for chunk in stream:
        if chunk.choices and chunk.choices[0].delta.content:
            for char in chunk.choices[0].delta.content:
                reply += char
                yield reply, None, "Generating..."
                time.sleep(0.005)
        if chunk.usage:
            usage = chunk.usage
    elapsed = time.perf_counter() - start
    text = clean_output(reply)

    path = "documented.py"
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    
    logic = check_logic(code, text)

    prompt_tokens = usage.prompt_tokens
    completion_tokens = usage.completion_tokens
    input_price, output_price = PRICES[model_name]
    input_cost = prompt_tokens / 1_000_000 * input_price
    output_cost = completion_tokens / 1_000_000 * output_price
    cost = input_cost + output_cost
    logic_tokenscost = f"{logic}  ·     Cost: ${cost:.4f}     ·     Time Taken:{elapsed:.2f} seconds   "
    yield text, path, logic_tokenscost

def load_file(path):
    with open(path) as f:
        text = f.read()
    return text


css = """
.code-box { min-height: 650px; }
.code-box .cm-editor { height: 600px; }
.code-box .cm-scroller { overflow: auto; }
"""

with gr.Blocks(fill_width=True, css=css) as ui:
    status = gr.Markdown()
    model_dropdown = gr.Dropdown(
        choices=list(MODELS.keys()),
        value="Gemini 3.5 Flash Lite",
        label="Model"
    )
    with gr.Row():
        code_box = gr.Code(language="python", label="Your code", elem_classes="code-box")
        output_box = gr.Code(language="python", label="Documented code", elem_classes="code-box")
    with gr.Row():
        upload = gr.UploadButton("Upload .py", file_types=[".py"], variant="secondary")
        go = gr.Button("Generate", variant="primary")
        download = gr.DownloadButton("Download", variant="secondary")

    go.click(generate, inputs=[code_box, model_dropdown], outputs=[output_box, download, status])
    upload.upload(load_file, inputs=upload, outputs=code_box)
    

ui.launch(inbrowser=True)


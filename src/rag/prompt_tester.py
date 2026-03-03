# src/rag/prompt_tester.py
"""
Tests all 4 prompt strategies against a real paper context using Claude.
Run directly:  python -m src.rag.prompt_tester
"""
import json
import os
import sys
import re
import anthropic

# Ensure UTF-8 output on Windows terminals
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from dotenv import load_dotenv

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from src.rag.prompts import PromptStrategy, build_prompt
from src.ingestion.pdf_extractor import extract_text_from_pdf
from src.ingestion.text_cleaner import clean_extracted_text

load_dotenv()

# ── Config ─────────────────────────────────────────────────────────────────
PAPERS_DIR   = "C:/Users/LENOVO/Documents/Papers"
TEST_PAPER   = "Gerschewski (2020).pdf"
TEST_QUESTION = (
    "What is the 'missing diagonal' identified by Gerschewski, "
    "and why is it important for understanding institutional change?"
)
CONTEXT_CHARS = 3000   # characters of paper text used as context
CLAUDE_MODEL  = "claude-sonnet-4-6"

# ── Helpers ────────────────────────────────────────────────────────────────

def load_context(paper_filename: str, max_chars: int) -> str:
    """Extract and clean a slice of text from a paper to use as RAG context."""
    path = os.path.join(PAPERS_DIR, paper_filename)
    result = extract_text_from_pdf(path)
    text = clean_extracted_text(result["text"])
    return text[:max_chars]


def call_claude(prompt: str, model: str = CLAUDE_MODEL) -> str:
    """Send a prompt to Claude and return the response text."""
    client = anthropic.Anthropic()
    message = client.messages.create(
        model=model,
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    )
    return message.content[0].text


def parse_v4_response(raw: str) -> dict:
    """Split V4 Chain-of-Thought response into reasoning + final answer."""
    reasoning, answer = "", raw
    if "FINAL ANSWER:" in raw:
        parts   = raw.split("FINAL ANSWER:", 1)
        reasoning = parts[0].replace("STEP-BY-STEP REASONING:", "").strip()
        answer    = parts[1].strip()
    return {"reasoning": reasoning, "final_answer": answer}


def parse_v2_response(raw: str) -> dict:
    """Extract JSON block from V2 structured response."""
    try:
        # Find the first {...} block in the response
        match = re.search(r'\{.*\}', raw, re.DOTALL)
        if match:
            return json.loads(match.group())
    except json.JSONDecodeError:
        pass
    return {"raw_response": raw, "parse_error": "Could not parse JSON"}


# ── Main test runner ───────────────────────────────────────────────────────

def run_tests():
    print("=" * 70)
    print("RESEARCH COPILOT - Prompt Strategy Tester")
    print("=" * 70)
    print(f"Paper:    {TEST_PAPER}")
    print(f"Question: {TEST_QUESTION}")
    print(f"Model:    {CLAUDE_MODEL}")
    print()

    context = load_context(TEST_PAPER, CONTEXT_CHARS)
    results = {}

    strategies = [
        (PromptStrategy.V1_BASIC,      "V1 — Basic Rules + APA"),
        (PromptStrategy.V2_STRUCTURED, "V2 — Structured JSON"),
        (PromptStrategy.V3_FEW_SHOT,   "V3 — Few-Shot Examples"),
        (PromptStrategy.V4_CHAIN,      "V4 — Chain of Thought"),
    ]

    for strategy, label in strategies:
        print("-" * 70)
        print(f"  {label}")
        print("-" * 70)

        prompt = build_prompt(strategy, context, TEST_QUESTION)
        raw    = call_claude(prompt)

        if strategy == PromptStrategy.V2_STRUCTURED:
            parsed = parse_v2_response(raw)
            results[strategy.value] = parsed
            print(json.dumps(parsed, indent=2, ensure_ascii=False))

        elif strategy == PromptStrategy.V4_CHAIN:
            parsed = parse_v4_response(raw)
            results[strategy.value] = parsed
            print(f"[REASONING]\n{parsed['reasoning'][:400]}...\n")
            print(f"[FINAL ANSWER]\n{parsed['final_answer']}")

        else:
            results[strategy.value] = raw
            print(raw)

        print()

    return results


if __name__ == "__main__":
    run_tests()

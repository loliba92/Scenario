#!/usr/bin/env python3
import json
import os
import sys
import time
import urllib.request
from pathlib import Path

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
REPO_ROOT = Path(__file__).resolve().parent.parent.parent

def load_brief(date_str):
    brief_path = REPO_ROOT / "editorial-briefs" / f"{date_str}.json"
    with open(brief_path) as f:
        return json.load(f)

def load_prompt():
    prompt_path = REPO_ROOT / "docs" / "routine-redaction-prompt.md"
    return prompt_path.read_text(encoding="utf-8")

def call_nemotron(brief, prompt, api_key, timeout=300):
    full_prompt = f"{prompt}\n\n=== BRIEF DU JOUR ===\n{json.dumps(brief, ensure_ascii=False, indent=2)}"
    
    body = json.dumps({
        "model": "nvidia/nemotron-3-ultra-550b-a55b:free",
        "max_tokens": 12000,
        "temperature": 0.45,
        "response_format": {"type": "json_object"},
        "messages": [{"role": "user", "content": full_prompt}],
    }).encode()
    
    req = urllib.request.Request(
        OPENROUTER_URL,
        method="POST",
        data=body,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
    )
    
    start = time.time()
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        response = json.loads(resp.read())
        elapsed = time.time() - start
        
        if "error" in response:
            raise Exception(f"OpenRouter error: {response['error']}")
        
        content = response["choices"][0]["message"]["content"]
        usage = response.get("usage", {})
        
        return {
            "content": content,
            "elapsed_s": elapsed,
            "cost": usage.get("cost"),
            "tokens_in": usage.get("prompt_tokens"),
            "tokens_out": usage.get("completion_tokens"),
        }

if __name__ == "__main__":
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        print("❌ OPENROUTER_API_KEY manquant", file=sys.stderr)
        sys.exit(1)
    
    brief = load_brief("2026-09-21")
    prompt = load_prompt()
    
    print("🔄 Appel NVIDIA Nemotron 3 Ultra pour rédaction...", file=sys.stderr)
    result = call_nemotron(brief, prompt, api_key)
    
    # Sauvegarder en JSON
    output = {
        "date": "2026-09-21",
        "model": "nvidia/nemotron-3-ultra-550b-a55b:free",
        "brief_subject": brief.get("sujet", {}).get("titre_propose"),
        "cost": result["cost"],
        "elapsed_s": result["elapsed_s"],
        "tokens": {
            "input": result["tokens_in"],
            "output": result["tokens_out"],
        },
        "redaction": json.loads(result["content"]),
    }
    
    output_path = REPO_ROOT / "docs" / "nemotron-redaction-2026-09-21.json"
    output_path.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n")
    
    print(f"\n✅ Redaction sauvegardée: {output_path}", file=sys.stderr)
    print(f"   Coût: ${result['cost']}", file=sys.stderr)
    print(f"   Temps: {result['elapsed_s']:.1f}s", file=sys.stderr)
    print(f"   Tokens: {result['tokens_in']} in / {result['tokens_out']} out", file=sys.stderr)

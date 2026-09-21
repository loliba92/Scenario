#!/usr/bin/env python3
import json
import os
import sys
import time
import urllib.request
from pathlib import Path

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
REPO_ROOT = Path(__file__).resolve().parent.parent.parent

MODELS = [
    {"id": "google/gemini-3.7-flash", "name": "Google Gemini 3.7 Flash"},
    {"id": "amazon/nova-micro-v1", "name": "Amazon Nova Micro v1"},
    {"id": "qwen/qwen3.5-397b-a17b", "name": "Qwen 3.5 (397B)"},
]

def load_brief():
    with open(REPO_ROOT / "editorial-briefs" / "2026-09-21.json") as f:
        return json.load(f)

def load_prompt():
    return (REPO_ROOT / "docs" / "routine-redaction-prompt.md").read_text()

def test_model(model_id, brief, prompt, api_key):
    full_prompt = f"{prompt}\n\n=== BRIEF DU JOUR ===\n{json.dumps(brief, ensure_ascii=False, indent=2)}"
    
    body = json.dumps({
        "model": model_id,
        "max_tokens": 12000,
        "temperature": 0.45,
        "response_format": {"type": "json_object"},
        "messages": [{"role": "user", "content": full_prompt}],
    }).encode()
    
    req = urllib.request.Request(
        OPENROUTER_URL,
        method="POST",
        data=body,
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
    )
    
    start = time.time()
    try:
        with urllib.request.urlopen(req, timeout=300) as resp:
            response = json.loads(resp.read())
            elapsed = time.time() - start
            
            if "error" in response:
                return {"success": False, "error": response["error"].get("message", "Unknown")}
            
            content = response["choices"][0]["message"]["content"]
            usage = response.get("usage", {})
            
            json_valid = False
            if content:
                try:
                    json.loads(content)
                    json_valid = True
                except:
                    pass
            
            return {
                "success": True,
                "cost": usage.get("cost"),
                "elapsed_s": elapsed,
                "tokens_in": usage.get("prompt_tokens"),
                "tokens_out": usage.get("completion_tokens"),
                "json_valid": json_valid,
                "content_length": len(content) if content else 0,
            }
    except Exception as e:
        return {"success": False, "error": str(e)}

if __name__ == "__main__":
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        print("❌ OPENROUTER_API_KEY manquant", file=sys.stderr)
        sys.exit(1)
    
    brief = load_brief()
    prompt = load_prompt()
    
    print("=" * 70)
    print("TEST ALTERNATIVES - RÉDACTION")
    print("=" * 70)
    print()
    
    results = {}
    for model_info in MODELS:
        model_id = model_info["id"]
        print(f"🔄 Test: {model_info['name']}...", file=sys.stderr)
        
        result = test_model(model_id, brief, prompt, api_key)
        results[model_id] = result
        
        print(f"\n{model_info['name']}")
        print(f"{'='*70}")
        
        if result["success"]:
            print(f"✅ SUCCESS")
            print(f"   Coût: ${result['cost']}")
            print(f"   Temps: {result['elapsed_s']:.1f}s")
            print(f"   Tokens: {result['tokens_in']} in / {result['tokens_out']} out")
            print(f"   JSON valide: {'✅ OUI' if result['json_valid'] else '❌ NON'}")
            print(f"   Taille réponse: {result['content_length']} caractères")
        else:
            print(f"❌ FAILED: {result['error']}")
        print()
    
    # Résumé
    print("=" * 70)
    print("RÉSUMÉ COMPARATIF")
    print("=" * 70)
    valid_models = [(m, results[m["id"]]) for m in MODELS if results[m["id"]]["success"] and results[m["id"]]["json_valid"]]
    
    if valid_models:
        print("\n✅ Modèles avec JSON valide:")
        for model_info, result in sorted(valid_models, key=lambda x: x[1]["cost"] if x[1]["cost"] else float("inf")):
            print(f"  - {model_info['name']:30} | ${result['cost']:8} | {result['elapsed_s']:6.1f}s")

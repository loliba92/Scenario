#!/usr/bin/env python3
"""
Comparateur de modèles OpenRouter pour la RÉDACTION.

Prend le brief du jour et teste la rédaction avec 4 modèles différents.
Compare coût, latence, et qualité du JSON généré.

Usage:
    export OPENROUTER_API_KEY=sk-or-v1-...
    python3 test-redaction-comparison.py --date 2026-09-21
"""

import json
import os
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime
from pathlib import Path

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
REPO_ROOT = Path(__file__).resolve().parent.parent.parent

MODELS_TO_TEST = [
    {
        "id": "nvidia/nemotron-3-ultra-550b-a55b:free",
        "name": "NVIDIA Nemotron 3 Ultra",
        "pricing": "$0/$0 (GRATUIT)",
        "category": "Free frontier reasoning",
    },
    {
        "id": "z-ai/glm-5.3-flash",
        "name": "GLM 5.3 Flash",
        "pricing": "? (à vérifier)",
        "category": "Research flash",
    },
    {
        "id": "tencent/hy4-preview",
        "name": "Tencent HY4 Preview",
        "pricing": "? (à vérifier)",
        "category": "Frontier preview",
    },
    {
        "id": "xiaomi/mimo-v2.5",
        "name": "Xiaomi MIMO v2.5",
        "pricing": "? (à vérifier)",
        "category": "Mobile-optimized",
    },
    {
        "id": "anthropic/claude-sonnet-5",
        "name": "Sonnet 5",
        "pricing": "$2/$10 (baseline)",
        "category": "Production",
    },
    {
        "id": "sakana/fugu-max",
        "name": "Sakana Fugu Max",
        "pricing": "$2/$6 (spécialisé)",
        "category": "Research",
    },
    {
        "id": "deepseek/deepseek-chat",
        "name": "DeepSeek v4",
        "pricing": "$0.12/$0.48 (ultra-budget)",
        "category": "Budget",
    },
]


def load_brief(date_str):
    """Charge le brief du jour."""
    brief_path = REPO_ROOT / "editorial-briefs" / f"{date_str}.json"
    if not brief_path.exists():
        raise FileNotFoundError(f"Brief absent : {brief_path}")
    with open(brief_path) as f:
        return json.load(f)


def load_prompt():
    """Charge le prompt de rédaction."""
    prompt_path = REPO_ROOT / "docs" / "routine-redaction-prompt.md"
    if not prompt_path.exists():
        raise FileNotFoundError(f"Prompt absent : {prompt_path}")
    return prompt_path.read_text(encoding="utf-8")


def call_model_redaction(model_id, brief, prompt, api_key, timeout=180):
    """Appelle un modèle pour la rédaction."""
    # Injecter le brief dans le prompt
    full_prompt = f"{prompt}\n\n=== BRIEF DU JOUR ===\n{json.dumps(brief, ensure_ascii=False, indent=2)}"

    body_dict = {
        "model": model_id,
        "max_tokens": 12000,
        "temperature": 0.45,
        "response_format": {"type": "json_object"},
        "usage": {"include": True},
        "messages": [{"role": "user", "content": full_prompt}],
    }

    # Désactiver reasoning pour Anthropic et DeepSeek
    if "anthropic/" in model_id or "deepseek/" in model_id:
        body_dict["reasoning"] = {"enabled": False}

    body = json.dumps(body_dict).encode()
    req = urllib.request.Request(
        OPENROUTER_URL,
        method="POST",
        data=body,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
    )

    result = {"model": model_id, "success": False, "error": None}
    start_time = time.time()

    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            response_data = json.loads(resp.read())
            elapsed = time.time() - start_time

            if "error" in response_data:
                result["error"] = response_data["error"].get("message", "Unknown error")
            else:
                result["success"] = True
                result["elapsed_s"] = elapsed
                result["usage"] = response_data.get("usage", {})
                result["cost"] = response_data.get("usage", {}).get("cost", "?")

                try:
                    content = response_data["choices"][0]["message"]["content"]
                    # Essayer de parser le JSON pour vérifier sa validité
                    parsed = json.loads(content)
                    result["json_valid"] = True
                    result["content_length"] = len(content)
                    # Extraire stats du JSON
                    if isinstance(parsed, dict):
                        result["json_keys"] = list(parsed.keys())
                except (json.JSONDecodeError, ValueError) as e:
                    result["json_valid"] = False
                    result["json_error"] = str(e)

                except (KeyError, IndexError, TypeError):
                    result["error"] = "Format réponse imprévu"

    except urllib.error.HTTPError as e:
        result["error"] = f"HTTP {e.code}: {e.reason}"
    except Exception as e:
        result["error"] = str(e)

    return result


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--date", required=True, help="Date du brief (AAAA-MM-JJ)")
    parser.add_argument("--dry-run", action="store_true", help="Afficher le prompt sans appeler OpenRouter")
    args = parser.parse_args()

    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key and not args.dry_run:
        print("❌ OPENROUTER_API_KEY manquant", file=sys.stderr)
        sys.exit(1)

    print("=" * 70)
    print("COMPARATEUR DE RÉDACTION - MODÈLES OPENROUTER")
    print("=" * 70)
    print(f"\nDate: {args.date}")

    # Charger brief et prompt
    try:
        brief = load_brief(args.date)
        prompt = load_prompt()
        print(f"✅ Brief chargé (sujet: {brief.get('sujet', {}).get('titre_propose', '?')})")
        print(f"✅ Prompt de rédaction chargé ({len(prompt)} caractères)")
    except FileNotFoundError as e:
        print(f"❌ {e}", file=sys.stderr)
        sys.exit(1)

    if args.dry_run:
        print("\n" + "=" * 70)
        print("MODE DRY-RUN (pas d'appel OpenRouter)")
        print("=" * 70)
        print(f"\nModèles à tester: {', '.join(m['name'] for m in MODELS_TO_TEST)}")
        print(f"Brief: {len(json.dumps(brief))} caractères")
        print(f"Prompt: {len(prompt)} caractères")
        print(f"\nCoût estimé: $0.10–0.50 (4 modèles × ~10k tokens)")
        print(f"Durée estimée: 5–10 minutes\n")
        print("Pour lancer le test réel:")
        print(f"  export OPENROUTER_API_KEY=sk-or-v1-...")
        print(f"  python3 test-redaction-comparison.py --date {args.date}")
        return

    print("\n" + "=" * 70)
    print("LANCEMENT DES TESTS")
    print("=" * 70)

    results = {}

    for model_info in MODELS_TO_TEST:
        model_id = model_info["id"]
        print(f"\n🔄 Test en cours: {model_info['name']}...", file=sys.stderr)

        result = call_model_redaction(model_id, brief, prompt, api_key)
        results[model_id] = result

        print(f"\n{'=' * 70}")
        print(f"{model_info['name']} ({model_info['pricing']})")
        print(f"{'=' * 70}")

        if result["success"]:
            print(f"✅ SUCCESS")
            print(f"   Coût: ${result['cost'] if result['cost'] != '?' else '?'}")
            print(f"   Temps: {result['elapsed_s']:.1f}s")
            print(f"   JSON valide: {result.get('json_valid', False)}")
            print(f"   Taille réponse: {result.get('content_length', '?')} caractères")
            if result.get("json_keys"):
                print(f"   Clés JSON: {', '.join(result['json_keys'][:5])}")
        else:
            print(f"❌ FAILED")
            print(f"   Erreur: {result['error']}")

        time.sleep(1)

    # Résumé
    print("\n" + "=" * 70)
    print("RÉSUMÉ COMPARATIF - RÉDACTION")
    print("=" * 70)

    success_models = [m for m in MODELS_TO_TEST if results[m["id"]]["success"]]
    failed_models = [m for m in MODELS_TO_TEST if not results[m["id"]]["success"]]

    if success_models:
        print("\n✅ Modèles fonctionnels:")
        for model_info in sorted(
            success_models, key=lambda m: results[m["id"]].get("cost", float("inf"))
        ):
            cost = results[model_info["id"]].get("cost", "?")
            time_s = results[model_info["id"]].get("elapsed_s", "?")
            json_ok = "✅" if results[model_info["id"]].get("json_valid") else "❌"
            print(f"  - {model_info['name']:20} | Coût: ${cost:6} | Temps: {time_s:5.1f}s | JSON: {json_ok}")

    if failed_models:
        print("\n❌ Modèles échoués:")
        for model_info in failed_models:
            print(f"  - {model_info['name']:20} | Erreur: {results[model_info['id']]['error']}")

    # Sauvegarder résultats
    report_path = Path(__file__).parent / "test-redaction-results.json"
    report = {
        "timestamp": datetime.now().isoformat(),
        "date": args.date,
        "brief_sujet": brief.get("sujet", {}).get("titre_propose", "?"),
        "models": [
            {
                "name": m["name"],
                "model_id": m["id"],
                "pricing": m["pricing"],
                "success": results[m["id"]]["success"],
                "cost": results[m["id"]].get("cost"),
                "elapsed_s": results[m["id"]].get("elapsed_s"),
                "json_valid": results[m["id"]].get("json_valid"),
                "error": results[m["id"]].get("error"),
            }
            for m in MODELS_TO_TEST
        ],
    }

    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(f"\n📊 Résultats sauvegardés: {report_path}")


if __name__ == "__main__":
    main()

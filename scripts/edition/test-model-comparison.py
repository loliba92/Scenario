#!/usr/bin/env python3
"""
Comparateur de modèles OpenRouter pour la tâche de recherche éditorial.

Teste plusieurs modèles (Haiku 4.5, Sakana Fugu Max, Sonnet 5, DeepSeek) sur la
même tâche de recherche simplifiée et compare:
- Qualité des réponses
- Temps d'exécution
- Coût réel
- Capacité à utiliser web_search

Usage:
    export OPENROUTER_API_KEY=sk-or-v1-...
    python3 test-model-comparison.py
"""

import json
import os
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timedelta
from pathlib import Path

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

# Modèles à tester avec leurs profils d'intérêt
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
        "id": "anthropic/claude-sonnet-5",
        "name": "Sonnet 5",
        "pricing": "$2/$10 (baseline actuel)",
        "category": "Anthropic production",
    },
    {
        "id": "sakana/fugu-max",
        "name": "Sakana Fugu Max",
        "pricing": "$2/$6 (web search intégré)",
        "category": "Research specialist",
    },
    {
        "id": "deepseek/deepseek-chat",
        "name": "DeepSeek v4",
        "pricing": "$0.12/$0.48 (95% moins cher)",
        "category": "Budget extreme",
    },
]

# Prompt de test : un cas réaliste simplifié de recherche quotidienne
TEST_PROMPT = """Tu dois effectuer une recherche rapide pour choisir un sujet d'actualité
à couvrir demain. Tu as accès à une recherche web en temps réel.

**Tâche:** Identifie 3 sujets d'actualité pertinents pour Scénario (site français de
scénarios chiffrés) qui:
1. Sont survenus dans les 7 derniers jours
2. Ont un impact économique/géopolitique mesurable
3. Ne sont pas des répétitions de sujets très récents

Pour chaque sujet, fournis:
- Titre en 10-15 mots
- Une question centrale (20-30 mots)
- Les 3 chiffres-clés (faits vérifiables avec sources web)

**Format réponse:** JSON uniquement, structure {
  "sujets": [
    {
      "titre": "...",
      "question": "...",
      "chiffres": ["fait1: source", "fait2: source", "fait3: source"],
      "domaine": "géopolitique|économie|tech|santé|énergie"
    }
  ],
  "timestamp_recherche": "ISO 8601"
}

Raisonne brièvement avant le JSON final (30-50 mots expliquant ton choix).
"""


def call_model(model_id, api_key, timeout=120):
    """Appelle un modèle via OpenRouter et mesure performance."""
    body_dict = {
        "model": model_id,
        "max_tokens": 2000,
        "temperature": 0.6,
        "response_format": {"type": "json_object"},
        "usage": {"include": True},  # Récupérer le coût réel
        "messages": [{"role": "user", "content": TEST_PROMPT}],
        "tools": [{"type": "openrouter:web_search", "parameters": {"engine": "auto", "max_results": 5}}],
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
                    result["response_preview"] = content[:200] + "..." if len(content) > 200 else content
                except (KeyError, IndexError, TypeError):
                    result["error"] = "Format réponse imprévu (pas de contenu)"

    except urllib.error.HTTPError as e:
        result["error"] = f"HTTP {e.code}: {e.reason}"
    except Exception as e:
        result["error"] = str(e)

    return result


def format_result(result, model_info):
    """Formate un résultat de test pour affichage."""
    status = "✅ SUCCESS" if result["success"] else "❌ FAILED"
    output = f"\n{'=' * 70}\n{model_info['name']} ({model_info['pricing']})\n{'=' * 70}"
    output += f"\nStatut: {status}"

    if result["success"]:
        output += f"\nTemps: {result['elapsed_s']:.1f}s"
        output += f"\nCoût: ${result['cost'] if result['cost'] != '?' else '?'}"
        usage = result.get("usage", {})
        output += f"\nTokens: {usage.get('prompt_tokens', '?')} in / {usage.get('completion_tokens', '?')} out"
        output += f"\nPréaperçu:\n{result.get('response_preview', 'N/A')}"
    else:
        output += f"\nErreur: {result['error']}"

    return output


def main():
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        print("❌ OPENROUTER_API_KEY manquant dans l'environnement", file=sys.stderr)
        sys.exit(1)

    print("=" * 70)
    print("COMPARATEUR DE MODÈLES OPENROUTER")
    print("Tâche: Recherche éditorial quotidienne (sujet + web search)")
    print("=" * 70)
    print(f"\nDate du test: {datetime.now().isoformat()}")
    print(f"Modèles à tester: {len(MODELS_TO_TEST)}\n")

    results = {}

    for model_info in MODELS_TO_TEST:
        model_id = model_info["id"]
        print(f"🔄 Test en cours: {model_info['name']}...", file=sys.stderr)

        result = call_model(model_id, api_key)
        results[model_id] = result
        model_info["result"] = result

        print(format_result(result, model_info))
        time.sleep(1)  # Éviter rate limiting

    # Résumé comparatif
    print("\n" + "=" * 70)
    print("RÉSUMÉ COMPARATIF")
    print("=" * 70)

    success_models = [m for m in MODELS_TO_TEST if m["result"]["success"]]
    failed_models = [m for m in MODELS_TO_TEST if not m["result"]["success"]]

    if success_models:
        print("\n✅ Modèles fonctionnels:")
        for model_info in sorted(success_models, key=lambda m: m["result"].get("cost", float("inf"))):
            cost = model_info["result"].get("cost", "?")
            time_s = model_info["result"].get("elapsed_s", "?")
            print(f"  - {model_info['name']:20} | Coût: ${cost:6} | Temps: {time_s}s")

    if failed_models:
        print("\n❌ Modèles échoués:")
        for model_info in failed_models:
            print(f"  - {model_info['name']:20} | Erreur: {model_info['result']['error']}")

    # Recommandation
    print("\n" + "=" * 70)
    print("RECOMMANDATION IMMÉDIATE")
    print("=" * 70)

    if success_models:
        best_cost = min(success_models, key=lambda m: m["result"].get("cost", float("inf")))
        best_speed = min(success_models, key=lambda m: m["result"].get("elapsed_s", float("inf")))
        best_combined = sorted(
            success_models,
            key=lambda m: (m["result"].get("cost", 1), m["result"].get("elapsed_s", 1000)),
        )[0]

        print(f"\n💰 Moins cher: {best_cost['name']} (${best_cost['result'].get('cost', '?')})")
        print(f"⚡ Plus rapide: {best_speed['name']} ({best_speed['result'].get('elapsed_s', '?'):.1f}s)")
        print(f"\n🎯 Meilleur rapport: {best_combined['name']}")
        print(f"   → Tester ce modèle sur 5 jours en production")
        print(f"   → Voir docs/recherche-modele-efficace.md pour le plan complet")

    else:
        print("\n❌ Tous les modèles ont échoué. Vérifier OPENROUTER_API_KEY et quotas.")

    # Sauvegarder les résultats
    report_path = Path(__file__).parent / "test-results.json"
    report = {
        "timestamp": datetime.now().isoformat(),
        "models": [
            {
                "name": m["name"],
                "model_id": m["id"],
                "pricing": m["pricing"],
                "category": m["category"],
                "success": m["result"]["success"],
                "cost": m["result"].get("cost", None),
                "elapsed_s": m["result"].get("elapsed_s", None),
                "error": m["result"].get("error", None),
            }
            for m in MODELS_TO_TEST
        ],
    }

    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(f"\n📊 Résultats sauvegardés: {report_path}")


if __name__ == "__main__":
    main()

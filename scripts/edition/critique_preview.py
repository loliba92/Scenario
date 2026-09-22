"""Critique éditoriale automatique du preview du lendemain, lancée juste
après la génération (voir .github/workflows/daily-preview.yml) — avant
même la relecture humaine de l'après-midi (docs/PREVIEW-WORKFLOW.md).

Root cause : l'édition du 22 septembre 2026 (crise Bab el-Mandeb/Ormuz)
est passée en production avec un prix du Brent périmé, une attribution
("selon JPMorgan") invérifiable, et une rupture de ton — 3 défauts que la
routine de rédaction avait la consigne de vérifier (docs/routine-prompt.md,
§ Anti-péremption / Relecture de cohérence / Relecture stylistique) mais
qu'aucune revue indépendante ne recroisait avant que le preview ne soit
proposé à la validation humaine. Ce script fait cette revue automatiquement,
avec un modèle DIFFÉRENT de celui qui a rédigé l'édition (voir --model),
pour éviter qu'un même biais de rédaction repasse inaperçu à travers son
propre regard.

**Volontairement scope "statique" seulement, jamais du fact-checking réel.**
Ce script tourne dans un contexte CI sans accès web fiable (pas de clé
WebSearch dédiée, pas de garantie de latence/coût maîtrisés en boucle
quotidienne) — il ne vérifie donc JAMAIS un chiffre contre la réalité
extérieure. Il vérifie uniquement ce qui est vérifiable en ne lisant QUE
le brief + le contenu de l'édition eux-mêmes :
  - cohérence interne (un même chiffre répété doit porter la même valeur
    ET la même date partout où il apparaît) ;
  - toute affirmation attribuée nommément à une entité identifiée doit
    correspondre à une source listée dans le brief ;
  - ruptures de ton oral/conversationnel dans un `.dek` ;
  - répétitions lexicales excessives ;
  - framing des probabilités (scénarios additionnés en un seul chiffre
    choc sans que chacun corresponde vraiment au mot utilisé) ;
  - qualité du `graphique_dc_chart` si présent (cohérence date/valeur
    avec les indicateurs, `raison` suffisamment étayée).
Un vrai fact-check (comme la revue manuelle du 22 septembre, avec
WebSearch) reste un exercice humain ou à la demande — ce script est un
filet de sécurité automatique et volontairement plus étroit, pas un
remplacement.

Usage :
    OPENROUTER_API_KEY=... python3 critique_preview.py --date 2026-09-23 \
        --out /tmp/critique.md
"""
import argparse
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from generate_daily_edition import call_openrouter, GenerationError  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parents[2]

# Modèle volontairement différent de celui qui rédige l'édition en Phase 2
# (anthropic/claude-sonnet-5, voir docs/modeles-openrouter.md) — un même
# modèle relisant sa propre production a plus de chances de laisser passer
# ses propres angles morts qu'un second regard. openai/gpt-5 choisi parmi
# les 3 modèles déjà validés dans ce dépôt (docs/modeles-openrouter.md) :
# déjà en prod ailleurs (hebdo.yml), donc pas un nouveau modèle non testé
# à introduire spécifiquement pour ce script.
CRITIQUE_MODEL = "openai/gpt-5"

CRITIQUE_PROMPT_TEMPLATE = """Tu es un critique journaliste, le plus exigeant \
de la rédaction. Tu relis l'édition ci-dessous AVANT sa mise en ligne, avec un \
regard qui n'a pas écrit une ligne de cette édition.

**Contrainte stricte : tu n'as aucun accès à internet dans cet exercice.** \
Tu ne dois JAMAIS vérifier un chiffre, une date ou un fait contre la réalité \
extérieure, et jamais prétendre le faire. Ta revue porte uniquement sur ce \
qui est vérifiable en lisant seulement les documents fournis ci-dessous :

1. **Cohérence interne des chiffres et de leurs dates.** Un même chiffre \
(prix, pourcentage, décompte) répété à plusieurs endroits (indicateurs, \
`.dek`, essentiel, phrase à retenir, cartes de scénarios, graphique) \
doit porter la même valeur ET la même date partout. Signale toute \
divergence, même si les valeurs concordent mais que les dates attachées \
diffèrent.

2. **Attribution vérifiable.** Toute affirmation attribuée nommément à une \
entité identifiée (banque, agence, institut, étude — ex. "selon X, ...") \
doit correspondre à une source listée dans `sources` ci-dessous. Si aucune \
source ne semble couvrir cette attribution précise, signale-le comme un \
chiffre potentiellement mal sourcé — sans jamais chercher à vérifier toi-même \
si l'attribution est vraie (tu ne peux pas), seulement si elle est *couverte* \
par au moins une des sources listées.

3. **Ton et registre.** Le corps analytique (`.dek`, encarts Comprendre) \
garde un registre analytique à la troisième personne. Signale toute rupture \
orale/conversationnelle ou adresse directe au lecteur qui casserait ce ton \
au milieu d'un paragraphe d'analyse (le tutoiement reste normal dans les \
éléments d'interface : essentiel, retenir-box, CTA — ne les signale pas).

4. **Répétitions lexicales.** Un même mot ou une même image répétés 3 fois \
ou plus sous des formes proches dans l'édition (hors termes techniques du \
lexique, répétés par nature).

5. **Framing des probabilités.** Si l'essentiel ou un résumé additionne \
plusieurs scénarios en un seul chiffre de synthèse (ex. "X% de risque de \
crise" en cumulant deux scénarios), vérifie que CHAQUE scénario additionné \
correspond vraiment au mot utilisé pour les regrouper (ex. un scénario \
d'adaptation/normalisation progressive ne devrait pas être compté comme \
une "crise" sans nuance).

6. **Graphique historique (`graphique_dc_chart`), si présent.** Le dernier \
point de la série doit porter la même valeur/date que le chiffre déjà cité \
dans les indicateurs. `raison` doit citer une source et un nombre de points \
concrets, jamais une affirmation générique.

Pour chaque défaut trouvé, cite l'extrait exact concerné. Si un point n'a \
rien à signaler, ne le mentionne pas — ne remplis jamais artificiellement \
la liste des `findings` pour donner l'impression d'avoir travaillé.

Réponds en JSON strict avec cette forme exacte :
{{
  "verdict": "publiable" | "a_corriger" | "a_revoir_en_profondeur",
  "resume": "1 à 2 phrases de synthèse globale",
  "findings": [
    {{
      "categorie": "coherence_dates" | "attribution" | "ton" | "repetition" | "framing_probabilites" | "graphique" | "autre",
      "gravite": "bloquant" | "mineur",
      "constat": "description précise du problème",
      "extrait": "citation exacte du passage concerné",
      "correction_proposee": "suggestion concrète de correction"
    }}
  ]
}}

=== BRIEF (editorial-briefs/{date}.json) ===
{brief_json}

=== CONTENU DE L'ÉDITION (.preview-content.json) ===
{content_json}
"""


def build_prompt(date_str, brief, content):
    # sources : seule la liste (titre + url), jamais le brief entier une
    # deuxième fois — déjà inclus via brief_json, pas la peine de dupliquer
    # le contexte, seulement de rendre le prompt lisible pour ce point précis.
    return CRITIQUE_PROMPT_TEMPLATE.format(
        date=date_str,
        brief_json=json.dumps(brief, ensure_ascii=False, indent=2),
        content_json=json.dumps(content, ensure_ascii=False, indent=2),
    )


def render_markdown(date_str, critique, model):
    verdict_label = {
        "publiable": "✅ Publiable en l'état",
        "a_corriger": "⚠️ Points à corriger avant mise en prod",
        "a_revoir_en_profondeur": "🛑 À revoir en profondeur",
    }.get(critique.get("verdict"), f"❓ Verdict inattendu : {critique.get('verdict')!r}")

    lines = [
        f"## Critique éditoriale automatique — édition du {date_str}",
        "",
        f"**Verdict : {verdict_label}**",
        "",
        critique.get("resume", "(pas de résumé fourni)"),
        "",
    ]

    findings = critique.get("findings") or []
    if not findings:
        lines.append("Aucun point signalé par la relecture automatique.")
    else:
        gravite_order = {"bloquant": 0, "mineur": 1}
        for f in sorted(findings, key=lambda f: gravite_order.get(f.get("gravite"), 2)):
            badge = "🔴 bloquant" if f.get("gravite") == "bloquant" else "🟡 mineur"
            lines.append(f"### [{f.get('categorie', 'autre')}] {badge}")
            lines.append(f"**Constat :** {f.get('constat', '')}")
            if f.get("extrait"):
                lines.append(f"> {f['extrait']}")
            if f.get("correction_proposee"):
                lines.append(f"**Correction proposée :** {f['correction_proposee']}")
            lines.append("")

    lines.append("---")
    lines.append(
        f"_Revue automatique, contrôles statiques uniquement (pas de fact-check web) — "
        f"modèle {model}. Ne remplace pas la relecture humaine de l'après-midi._"
    )
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", required=True, help="AAAA-MM-JJ, date de l'édition à critiquer")
    parser.add_argument("--brief", help="Chemin du brief (défaut : editorial-briefs/{date}.json)")
    parser.add_argument("--content", help="Chemin du contenu (défaut : .preview-content.json)")
    parser.add_argument("--model", default=CRITIQUE_MODEL)
    parser.add_argument("--out", help="Fichier markdown de sortie (défaut : stdout)")
    parser.add_argument("--out-json", help="Fichier JSON brut de sortie (optionnel)")
    args = parser.parse_args()

    brief_path = Path(args.brief) if args.brief else REPO_ROOT / "editorial-briefs" / f"{args.date}.json"
    content_path = Path(args.content) if args.content else REPO_ROOT / ".preview-content.json"

    if not brief_path.exists():
        raise GenerationError(f"brief introuvable : {brief_path}")
    if not content_path.exists():
        raise GenerationError(f"contenu introuvable : {content_path}")

    brief = json.loads(brief_path.read_text(encoding="utf-8"))
    content = json.loads(content_path.read_text(encoding="utf-8"))

    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        raise GenerationError("OPENROUTER_API_KEY manquant dans l'environnement")

    prompt = build_prompt(args.date, brief, content)
    # max_tokens=16000 : openai/gpt-5 (modèle par défaut) impose son
    # raisonnement interne et refuse qu'on le désactive (voir le docstring
    # de call_openrouter()) — un budget trop court laisse le raisonnement
    # manger tout l'espace avant le JSON final (même incident déjà rencontré
    # sur generate_weekly_recap.py, qui utilise la même valeur pour ce cas).
    critique = call_openrouter(prompt, args.model, api_key, temperature=0.2, max_tokens=16000)

    markdown = render_markdown(args.date, critique, args.model)

    if args.out:
        Path(args.out).write_text(markdown, encoding="utf-8")
    else:
        print(markdown)

    if args.out_json:
        Path(args.out_json).write_text(json.dumps(critique, ensure_ascii=False, indent=2), encoding="utf-8")

    # Toujours un exit 0 : cette revue est un avis, jamais une porte
    # bloquante du pipeline — même en cas de verdict "a_revoir_en_profondeur",
    # le preview reste généré et attend la décision humaine habituelle.
    print(f"[critique] verdict : {critique.get('verdict')!r}", file=sys.stderr)


if __name__ == "__main__":
    main()

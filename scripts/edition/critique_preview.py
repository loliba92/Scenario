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
# ses propres angles morts qu'un second regard. deepseek/deepseek-v4-flash
# choisi pour le coût (le moins cher des 3 modèles validés dans ce dépôt,
# voir docs/modeles-openrouter.md) — retour utilisateur explicite, ce
# script tourne quotidiennement, jamais une fois par semaine comme
# hebdo.yml (openai/gpt-5). **Faiblesse documentée à connaître** :
# troncature/segments manquants sur du texte long et structuré (cause de
# son remplacement par Sonnet 5 sur translate_daily.py/generate_suivi_
# update.py, voir docs/modeles-openrouter.md § deepseek/deepseek-v4-flash)
# — mitigé ici en réduisant le brief au strict nécessaire avant de
# construire le prompt (voir build_prompt() / TRIMMED_BRIEF_KEYS), jamais
# en envoyant le brief complet comme le ferait un modèle plus robuste au
# texte long.
CRITIQUE_MODEL = "deepseek/deepseek-v4-flash"

# Champs du brief réellement utiles à CETTE critique (cohérence des
# chiffres déjà publiés, attribution contre les sources, cohérence du
# graphique) — jamais le brief complet (faits_verifies/acteurs/
# chronologie_cle/scenarios_prospectifs/elements_incertains/revue_de_
# presse/recommandations_redaction sont du matériau de RECHERCHE, pas
# des éléments que le contenu publié doit rester cohérent avec au sens
# de cette critique). Réduit le prompt d'environ moitié (~17K → ~6K
# caractères sur l'édition du 22 septembre) — la marge de sécurité qui
# compte le plus face à la faiblesse connue de DeepSeek sur le texte
# long, plus efficace qu'augmenter max_tokens en sortie.
TRIMMED_BRIEF_KEYS = ("sources", "indicateurs_kpi", "graphique_dc_chart")

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

=== SOURCES, INDICATEURS ET GRAPHIQUE DU BRIEF (editorial-briefs/{date}.json — champs {trimmed_keys}) ===
{brief_json}

=== CONTENU DE L'ÉDITION (.preview-content.json) ===
{content_json}
"""


def build_prompt(date_str, brief, content):
    trimmed_brief = {k: brief[k] for k in TRIMMED_BRIEF_KEYS if k in brief}
    return CRITIQUE_PROMPT_TEMPLATE.format(
        date=date_str,
        trimmed_keys=", ".join(TRIMMED_BRIEF_KEYS),
        brief_json=json.dumps(trimmed_brief, ensure_ascii=False, indent=2),
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
    # max_tokens : même repli que generate_weekly_recap.py::call_openrouter_json()
    # (docstring de call_openrouter() pour le détail des 2 incidents réels
    # qui ont fixé ces deux valeurs) — 4000 suffit pour deepseek/anthropic
    # (raisonnement désactivable, tout le budget sert au JSON final) ; un
    # modèle passé en --model dont le raisonnement est obligatoire (ex.
    # openai/gpt-5) a besoin de 16000, sous peine de renvoyer un contenu vide.
    can_disable_reasoning = "anthropic/" in args.model or "deepseek/" in args.model
    max_tokens = 4000 if can_disable_reasoning else 16000
    critique = call_openrouter(prompt, args.model, api_key, temperature=0.2, max_tokens=max_tokens)

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

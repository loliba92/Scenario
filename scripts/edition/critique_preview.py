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

# google/gemini-3.7-flash : même modèle que generate_daily_edition.py Phase 2.
# Choisi pour le coût ($0.0222) ET pour la fiabilité JSON validée à 100%
# en production (voir generate_daily_edition.py line 45-50 : "JSON valide 100%").
# DeepSeek avait une faiblesse sur la génération structurée (verdict=null
# incident du 22 septembre 2026), Gemini n'a pas ce problème observé.
# Un regard différent de celui du rédacteur reste souhaitable, mais Gemini
# est suffisamment distinct de Gemini pour la critique (modèle/température
# différents au minimum), et on gagne en fiabilité JSON.
CRITIQUE_MODEL = "google/gemini-3.7-flash"

# Champs du brief réellement utiles à CETTE critique (cohérence des
# chiffres déjà publiés, attribution contre les sources, cohérence du
# graphique) — jamais le brief complet (faits_verifies/acteurs/
# scenarios_prospectifs/elements_incertains/revue_de_presse/
# recommandations_redaction sont du matériau de RECHERCHE, pas des
# éléments que le contenu publié doit rester cohérent avec au sens de
# cette critique). Réduit le prompt d'environ moitié (~17K → ~6,8K
# caractères sur l'édition du 22 septembre) — la marge de sécurité qui
# compte le plus face à la faiblesse connue de DeepSeek sur le texte
# long, plus efficace qu'augmenter max_tokens en sortie.
# `chronologie_cle` ajouté après le premier test réel (22 septembre
# 2026) : sans lui, la critique a signalé la date du 18 septembre (prise
# de l'île de Perim) comme non sourcée dans le `.dek`, alors qu'elle est
# bien documentée dans le brief — juste pas dans un champ qu'on lui
# donnait à lire. Faux positif de trimming, pas un vrai défaut de
# l'édition. Coût négligeable (~650 caractères sur cette édition).
TRIMMED_BRIEF_KEYS = ("sources", "indicateurs_kpi", "graphique_dc_chart", "chronologie_cle")

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

7. **Style naturel, fluide et clair — jamais de tournure « IA ».** Relis \
chaque phrase du `dek`, des encarts Comprendre et de `why` comme si tu la \
disais à voix haute dans une conversation normale (même règle que celle \
donnée au rédacteur, docs/routine-redaction-prompt.md § « Jamais de \
tournure qui sonne artificielle »). Signale :
   - une affirmation suivie d'une négation abrupte ("X sert de Y... Ce \
n'est plus vrai : [fait]." — au lieu d'une structure concessive directe \
"D'ordinaire, [mécanisme]. Mais le [date], [fait].") ;
   - une subordonnée enchâssée au milieu d'une phrase, qui casse l'ordre \
naturel de lecture ;
   - des connecteurs lourds empilés ("de fait", "il convient de noter \
que", "en effet", "par ailleurs") là où un connecteur simple, ou rien du \
tout, suffirait ;
   - une double négation évitable ("n'est pas sans incidence sur" au lieu \
de "pèse sur") ;
   - une formule creuse ou trop symétrique ("il ne s'agit pas seulement de \
X, mais aussi de Y") qui n'apporte aucune information supplémentaire ;
   - un abus de vocabulaire sensationnaliste ("choc", "historique", \
"inédit", "paralysé", "catastrophe", "menace existentielle", "chaos", \
"jamais vu") plutôt qu'un vocabulaire d'analyse ("point de bascule", \
"pression", "risque", "levier", "dépendance", "rupture", "escalade", \
"vulnérabilité", "signal", "indicateur").
   Ne signale que ce qui casse réellement la fluidité ou la clarté de \
lecture — jamais une reformulation cosmétique sans gain réel.

8. **Titre (`h1`) court et percutant.** Le `h1` ne doit JAMAIS être la \
reprise telle quelle d'une phrase longue et descriptive (plus de 100 \
caractères) — un titre d'édition reste court et direct, jamais une \
sous-question complète. Si le `h1` dépasse cette longueur ou ressemble à \
une simple reformulation de `question_text` plutôt qu'à un vrai titre, \
signale-le et propose un `h1` court et percutant de remplacement (voir \
les h1 des éditions passées pour le ton attendu, ex. « Dollar : la fin du \
règne ? », « Budget 2027 : le gouvernement va-t-il tenir cet automne ? »).

Pour chaque défaut trouvé, cite l'extrait exact concerné. Si un point n'a \
rien à signaler, ne le mentionne pas — ne remplis jamais artificiellement \
la liste des `findings` pour donner l'impression d'avoir travaillé.

Réponds en JSON strict avec cette forme exacte. Le champ "verdict" DOIT être \
l'une de ces trois valeurs exactes : "publiable", "a_corriger", ou \
"a_revoir_en_profondeur" — jamais null, jamais vide, toujours l'une \
de ces trois chaînes exactes.

{{
  "verdict": "publiable",
  "resume": "1 à 2 phrases de synthèse globale",
  "findings": [
    {{
      "categorie": "coherence_dates",
      "gravite": "bloquant",
      "constat": "description précise du problème",
      "extrait": "citation exacte du passage concerné",
      "correction_proposee": "suggestion concrète de correction"
    }}
  ]
}}

Les valeurs possibles pour "verdict" sont EXACTEMENT :
  - "publiable" : l'édition est correcte et peut être publiée
  - "a_corriger" : l'édition a des points mineures à corriger
  - "a_revoir_en_profondeur" : l'édition a des problèmes importants

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


_NO_ISSUE_CORRECTION_PREFIXES = (
    "aucune correction",
    "pas de correction",
    "rien à corriger",
    "correction non nécessaire",
    "aucune",
    "aucun",
)


def validate_verdict(critique):
    """Valide que le verdict est l'une des trois valeurs acceptées.
    Lève une exception si le verdict est invalide (None, chaîne vide, etc.)."""
    valid_verdicts = {"publiable", "a_corriger", "a_revoir_en_profondeur"}
    verdict = critique.get("verdict")
    if verdict not in valid_verdicts:
        raise GenerationError(
            f"Verdict invalide du modèle : {verdict!r}. Attendu l'une de : {valid_verdicts}"
        )
    return critique


def drop_empty_findings(critique):
    """DeepSeek suit sa checklist de façon mécanique plutôt que d'omettre un
    point sans rien à signaler (voir consigne « ne jamais remplir
    artificiellement la liste des findings » dans CRITIQUE_PROMPT_TEMPLATE)
    — constaté sur 3 vrais runs successifs (22 septembre 2026, édition du
    même jour) : plusieurs « findings » disaient explicitement dans leur
    propre `constat` ('Aucun problème.', 'L'attribution est correcte.')
    n'avoir rien trouvé, tout en restant classés 🔴 bloquant. Signal
    identifié dans les données réelles plutôt que du pattern-matching sur
    le `constat` (trop variable) : un vrai défaut vient TOUJOURS avec une
    `correction_proposee` concrète ; un point vérifié et jugé sans problème
    a soit un champ vide (run 2), soit une formule figée du type « Aucune
    correction nécessaire » (run 3) — le modèle n'est pas cohérent d'un
    run à l'autre sur LEQUEL des deux il produit, donc les deux motifs
    sont filtrés. Filtré ici plutôt que de complexifier encore le prompt —
    un garde-fou côté code est plus fiable qu'une consigne supplémentaire
    sur un modèle déjà connu pour un suivi d'instructions imparfait sur ce
    genre de tâche.

    4e run réel (22 septembre 2026, run #20, issue #68, ajout du critère
    style_ia) : 2 findings avec `correction_proposee` = "Aucune." tout
    court (jamais "aucune correction...", le préfixe qui existait jusque-là
    ne matchait pas) sont passés à travers ce filtre. "aucune"/"aucun" seuls
    ajoutés aux préfixes plutôt qu'une liste de formules figées de plus en
    plus longue — cette famille de réponses commence toujours par ce mot,
    quelle que soit la suite exacte."""
    findings = critique.get("findings") or []
    kept = []
    for f in findings:
        correction = (f.get("correction_proposee") or "").strip()
        if not correction:
            continue
        if correction.lower().startswith(_NO_ISSUE_CORRECTION_PREFIXES):
            continue
        kept.append(f)
    dropped = len(findings) - len(kept)
    if dropped:
        print(f"[critique] {dropped} finding(s) sans correction proposée écartés (auto-signalés sans problème réel)", file=sys.stderr)
    critique["findings"] = kept
    return critique


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
    # call_openrouter() renvoie (content, usage) — voir sa dernière ligne
    # dans generate_daily_edition.py — jamais juste le contenu seul. Bug
    # réel trouvé au premier test local (22 septembre 2026, run sur
    # l'édition du même jour) : le premier essai de ce script affectait
    # directement le tuple à `critique`, provoquant un AttributeError dès
    # render_markdown() malgré un appel OpenRouter réussi côté serveur
    # (coût facturé, réponse reçue) — jamais détecté par les tests locaux
    # précédents, qui appelaient render_markdown() avec un dict simulé au
    # lieu du vrai retour de call_openrouter().
    critique, _usage = call_openrouter(prompt, args.model, api_key, temperature=0.2, max_tokens=max_tokens)
    critique = validate_verdict(critique)
    critique = drop_empty_findings(critique)

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

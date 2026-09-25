# Intégration SEO dans la routine de génération

## 🎯 Objectif
Automatiser la génération de métadonnées SEO optimisées pour chaque édition, sans intervention manuelle.

---

## 📍 Points d'intégration

### 1. **Dans `generate_daily_edition.py`** (après la rédaction)

Ajouter après la ligne où le brief est produit :

```python
# Après rédaction des contenus (actuelle Étape 3)
from scripts.edition.seo_optimizer import generate_seo_metadata

# ... code existant ...

# Générer métadonnées SEO
seo_data = generate_seo_metadata(brief, domain="sciences")  # adapter domain

# Injecter dans le brief pour transmission à build_html.py
brief["title"] = seo_data["title"]  # remplace H1 dans <title>
brief["meta_description"] = seo_data["meta_description"]
brief["keywords"] = seo_data["keywords"]
brief["newsarticle_json"] = seo_data["newsarticle_json"]
brief["breadcrumb_json"] = seo_data["breadcrumb_json"]
```

### 2. **Dans `build_html.py`** (génération du HTML)

#### A. Injecter le JSON-LD complet

Remplacer la ligne `def _build_head_per_day()` (ligne 187-220) :

```python
def _build_head_per_day(meta, domain, canonical_url, og_image, og_image_width, og_image_height, og_image_alt):
    # ... code existant ...
    
    # Récupérer JSON-LD du brief (si disponible)
    newsarticle_json = meta.get("newsarticle_json", "")
    breadcrumb_json = meta.get("breadcrumb_json", "")
    
    # Injecter les deux scripts JSON-LD
    json_ld_scripts = ""
    if newsarticle_json:
        json_ld_scripts += f"<script type=\"application/ld+json\">\n{newsarticle_json}\n</script>\n"
    if breadcrumb_json:
        json_ld_scripts += f"<script type=\"application/ld+json\">\n{breadcrumb_json}\n</script>\n"
    
    # Ajouter keywords meta tag
    keywords = meta.get("keywords", [])
    keywords_meta = ""
    if keywords:
        keywords_str = ", ".join(keywords)
        keywords_meta = f'<meta name="keywords" content="{keywords_str}">\n'
    
    # Retourner le tout
    return f"""<title>{title}</title>
...
{keywords_meta}
{json_ld_scripts}
"""
```

#### B. Ajouter la ligne auteur/date visible (dans le contenu)

Dans `_build_hero_section()`, après le `<h1>`, ajouter :

```python
def _build_hero_section(content, domain, date_str, eyebrow_text, author="Olivier Bertrand"):
    # ... code existant pour H1 ...
    
    # Ajouter ligne auteur/date
    author_line = f'<p class="article-meta">Par <strong>{author}</strong> — Publié le {date_fr} — Article informatif fondé sur données scientifiques et réglementaires.</p>'
    
    # ... reste du code ...
```

---

## 🔧 Modifications du prompt de rédaction

### Dans `docs/routine-redaction-prompt.md`

**Ajouter une instruction explicite sur la clarification des probabilités :**

```markdown
### Clarté des probabilités dans "L'essentiel"

Quand tu mentions un pourcentage de probabilité (ex: 50 %), clarifie toujours
son contexte dans la même phrase :

❌ **Éviter** : "Avec 50 % de probabilité, ces médicaments resteront réservés..."
✅ **Préférer** : "Notre scénario le plus probable (50 %) voit ces médicaments rester réservés..."

Cela rappelle au lecteur que ce sont des évaluations de la rédaction, pas des
faits certains. Mentionne les autres scénarios aussi si possible.
```

---

## 🧪 Checklist d'intégration

- [ ] Tester `seo_optimizer.py` en isolation (script `__main__`)
- [ ] Ajouter import dans `generate_daily_edition.py`
- [ ] Intégrer appel `generate_seo_metadata()` après rédaction
- [ ] Passer les métadonnées au brief JSON
- [ ] Modifier `build_html.py` pour injecter JSON-LD + keywords
- [ ] Tester sur une édition de test (générer HTML complet)
- [ ] Vérifier dans browser : title SEO + meta tags + structured data
- [ ] Valider JSON-LD avec https://schema.org/validator
- [ ] Pousser sur `main` dans une branche SEO

---

## 📊 Impact attendu

| Métrique | Avant | Après | Impact |
|----------|-------|-------|--------|
| Title SEO optimisé | Manuel | Auto | ✅ 100% éditions |
| Meta description | Manuel | Auto | ✅ 100% éditions |
| JSON-LD NewsArticle | Partiel | Complet | ✅ Indexation Google |
| BreadcrumbList | Absent | Présent | ✅ Rich snippets |
| Keywords meta | Absent | Présent | ✅ Contexte sémantique |
| Maillage interne | Partiel | À étendre | ⏳ Phase 2 |

---

## ⚠️ Limites actuelles (Phase 1)

Ce qu'on **n'automatise PAS** (trop coûteux pour le moment) :

1. **Maillage dynamique vers d'autres articles** — demande base de référence thématique
2. **Extraction intelligente de sources clés** — trop de faux positifs
3. **Génération de FAQ schema** — pas assez d'éditions pour pattern mining
4. **Optimisation pour Google News** — dépend de l'indexation déjà existante

→ À traiter en **Phase 2** si les résultats de Phase 1 sont convaincants.


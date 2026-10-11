# Modules « claude-seo » et « claude-blog » (import tiers)

Importés le 11 octobre 2026 depuis deux dépôts publics d'AgriciDaniel, sous licence MIT.

| Dépôt | Version importée | Modules |
|---|---|---|
| https://github.com/AgriciDaniel/claude-seo | commit `4b99de2` (v2.4.2) | `seo`, `seo-page`, `seo-technical`, `seo-content`, `seo-schema`, `seo-sitemap`, `seo-hreflang`, `seo-geo`, `seo-sxo`, `seo-plan`, `seo-cluster`, `seo-content-brief`, `seo-agentic` |
| https://github.com/AgriciDaniel/claude-blog | commit `2500d4c` | `blog`, `blog-write`, `blog-rewrite`, `blog-brief`, `blog-outline`, `blog-factcheck`, `blog-seo-check`, `blog-schema`, `blog-geo`, `blog-audit`, `blog-strategy`, `blog-cluster`, `blog-style`, `blog-analyze` |

Agents importés dans `.claude/agents/` : `seo-technical`, `seo-content`, `seo-schema`, `seo-sitemap`, `seo-geo`, `seo-sxo`, `seo-agentic`, `seo-cluster`, `blog-researcher`, `blog-reviewer`, `blog-seo`, `blog-writer`.

## Ce qui n'a PAS été importé, et pourquoi
- **Tout le code** : scripts Python, installateurs, hooks. Un hook s'exécute à chaque modification de fichier ; ce n'est pas du texte. Plusieurs modules citent des commandes `python scripts/…` : **ne pas les exécuter**, utiliser les outils habituels (lecture, récupération de page) ou demander au propriétaire.
- **`claude-ads`** (publicité payante) : Scénario ne fait pas de publicité payante. À importer plus tard si le besoin apparaît.
- **`seo-programmatic`** : la production de pages en série est précisément ce que les règles de Google sur le spam visent. Volontairement exclu.
- `seo-audit` de claude-seo : le dépôt contient déjà `seo-audit` (import marketingskills, voir `MARKETINGSKILLS.md`).
- Modules liés à des API payantes ou à des comptes (`seo-dataforseo`, `seo-backlinks`, `seo-google`, `seo-local`, `seo-maps`, `seo-ecommerce`…), à la génération d'images, ou à la traduction (le site a déjà son circuit).
- Le gabarit HTML `seo-cluster/templates/` (il contient un script) et les fichiers `LICENSE.txt` de chaque module (la licence figure ci-dessous).

## Modifications faites aux fichiers importés
- L'outil **`Bash` a été retiré** de la liste `tools:` des 8 agents SEO, pour qu'ils ne puissent pas lancer de commandes. Aucune autre modification.
- Les modules `seo` et `blog` (chefs d'orchestre) citent des sous-modules non importés : ces renvois sont sans effet.

## Règles d'usage dans ce dépôt
1. **`CLAUDE.md` l'emporte toujours** : vouvoiement, ton naturel et pédagogique, éditions passées figées, contrôle visuel avant livraison. Les modules `blog-*` écrivent des articles de blog : ils ne remplacent pas le circuit de rédaction des éditions de Scénario.
2. Le contexte du site est dans `.claude/product-marketing.md`.
3. Les attributions imposées par `claude-blog` (méthodes adaptées d'un autre projet sous licence Apache 2.0) sont dans `NOTICE-claude-blog.txt`.
4. Mise à jour : relire les dépôts source, comparer, remplacer. Ne pas modifier ces fichiers sur place.

## Licence d'origine (MIT)
Copyright (c) 2026 agricidaniel (claude-seo) ; Copyright (c) 2025-2026 AgriciDaniel (claude-blog).

Copyright (c) 2026 agricidaniel

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

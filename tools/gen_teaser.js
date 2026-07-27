const fs = require('fs');
const path = require('path');

const edition = {
  num: "N°04",
  dateShort: "27.07.2026",
  eyebrow: "Lundi · Géopolitique internationale",
  cover: "Iran–États-Unis : accord durable, trêve sous tension, ou reprise de la guerre ?",
  scenarios: [
    { accent: "#5e9c78", emoji: "🕊️", title: "Un accord verrouille la trêve" },
    { accent: "#6f8fae", emoji: "⚖️", title: "Ni guerre ni paix, la trêve traîne" },
    { accent: "#bd6248", emoji: "🔥", title: "Les combats reprennent, Ormuz se ferme" },
  ]
};

const LOGO = `<svg viewBox="0 0 120 120" xmlns="http://www.w3.org/2000/svg" fill="none" stroke-width="4.6" stroke-linecap="round" stroke-linejoin="round" style="width:56px;height:56px;flex:none">
  <path d="M57,96 L57,70 Q57,65 60,63" stroke="#cf9d4c"/><path d="M63,96 L63,70 Q63,65 60,63" stroke="#cf9d4c"/>
  <path d="M60,63 L60,55" stroke="#cf9d4c"/><path d="M60,55 L60,31" stroke="#6f8fae"/><path d="M55.8,38.9 L60,31 L64.2,38.9" stroke="#6f8fae"/>
  <path d="M60,63 L53.4,56.9" stroke="#cf9d4c"/><path d="M53.4,56.9 L34,39" stroke="#5e9c78"/><path d="M36.97,47.5 L34,39 L42.69,41.3" stroke="#5e9c78"/>
  <path d="M60,63 L66.6,56.9" stroke="#cf9d4c"/><path d="M66.6,56.9 L86,39" stroke="#bd6248"/><path d="M83.03,47.5 L86,39 L77.31,41.3" stroke="#bd6248"/></svg>`;

const BASE = `
  *{margin:0;padding:0;box-sizing:border-box;}
  html,body{width:1080px;height:1080px;}
  body{background:#10151c;color:#ece7da;font-family:"Inter","DejaVu Sans",sans-serif;-webkit-font-smoothing:antialiased;}
  .slide{width:1080px;height:1080px;padding:80px;display:flex;flex-direction:column;position:relative;overflow:hidden;}
  .accentbar{position:absolute;top:0;left:0;right:0;height:14px;}
  .topbar{display:flex;justify-content:space-between;align-items:center;border-bottom:1px solid #2c3644;padding-bottom:24px;}
  .brand{display:flex;align-items:center;gap:16px;}
  .wordmark{font-family:"Fraunces","DejaVu Serif",Georgia,serif;font-weight:700;font-size:42px;}
  .wordmark span{color:#cf9d4c;}
  .meta{font-family:"JetBrains Mono","DejaVu Sans Mono",monospace;font-size:24px;color:#a9a89c;letter-spacing:0.05em;}
  .kicker{font-family:"JetBrains Mono","DejaVu Sans Mono",monospace;font-size:25px;letter-spacing:0.14em;text-transform:uppercase;color:#cf9d4c;}
  .serif{font-family:"Fraunces","DejaVu Serif",Georgia,serif;font-weight:600;color:#ece7da;}
  .footer{margin-top:auto;display:flex;justify-content:space-between;align-items:center;font-family:"JetBrains Mono","DejaVu Sans Mono",monospace;font-size:24px;color:#a9a89c;}
  .dim{color:#a9a89c;}
`;

function page(inner){
  return `<!DOCTYPE html><html lang="fr"><head><meta charset="UTF-8">
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600;9..144,700&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">
<style>${BASE}</style></head><body>${inner}</body></html>`;
}
function topbar(){
  return `<div class="topbar"><div class="brand">${LOGO}<div class="wordmark">Scéna<span>rio</span></div></div><div class="meta">${edition.num} · ${edition.dateShort}</div></div>`;
}

function cover(){
  return page(`<div class="slide"><div class="accentbar" style="background:#cf9d4c"></div>${topbar()}
    <div class="kicker" style="margin-top:78px">${edition.eyebrow}</div>
    <div class="kicker" style="margin-top:60px;color:#cf9d4c">❓ La question du jour</div>
    <div class="serif" style="font-size:64px;line-height:1.16;margin-top:26px">${edition.cover}</div>
    <div class="footer"><div></div><div>Glisse&nbsp;→</div></div></div>`);
}

function scenarios(){
  const rows = edition.scenarios.map(s => `
    <div style="display:flex;align-items:center;gap:28px;border-left:7px solid ${s.accent};padding:6px 0 6px 28px">
      <span style="font-size:56px;line-height:1">${s.emoji}</span>
      <span class="serif" style="font-size:46px;line-height:1.12">${s.title}</span>
    </div>`).join('');
  return page(`<div class="slide"><div class="accentbar" style="background:#cf9d4c"></div>${topbar()}
    <div class="kicker" style="margin-top:70px">Trois scénarios possibles</div>
    <div style="display:flex;flex-direction:column;gap:44px;margin-top:60px">${rows}</div>
    <div class="serif" style="font-size:44px;color:#cf9d4c;margin-top:64px">Lequel est le plus probable&nbsp;?</div>
    <div class="footer"><div></div><div>Glisse&nbsp;→</div></div></div>`);
}

function cta(){
  return page(`<div class="slide"><div class="accentbar" style="background:#cf9d4c"></div>${topbar()}
    <div style="margin-top:150px">
      <div class="kicker">Le décryptage complet</div>
      <div class="serif" style="font-size:70px;line-height:1.12;margin-top:26px">Les 3 prévisions<br>chiffrées t'attendent</div>
      <div class="dim" style="font-size:34px;line-height:1.4;margin-top:30px;max-width:840px">Probabilités, indicateurs, et l'impact concret sur la France.</div>
    </div>
    <div style="margin-top:66px;display:flex;align-items:center;gap:22px">
      <span style="font-size:56px">🔗</span>
      <span class="serif" style="font-size:60px;color:#cf9d4c">Lien en bio</span>
    </div>
    <div style="margin-top:26px;font-family:'JetBrains Mono','DejaVu Sans Mono',monospace;font-size:31px;color:#5e9c78;letter-spacing:0.02em">✓ 100&nbsp;% gratuit, sans inscription</div>
    <div class="footer"><div></div><div></div></div></div>`);
}

const outDir = process.argv[2] || ".";
fs.mkdirSync(outDir, {recursive:true});
fs.writeFileSync(path.join(outDir,"01-question.html"), cover());
fs.writeFileSync(path.join(outDir,"02-scenarios.html"), scenarios());
fs.writeFileSync(path.join(outDir,"03-cta.html"), cta());
console.log("teaser slides écrits dans", outDir);

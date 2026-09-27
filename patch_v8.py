html = open('index.html', encoding='utf-8').read().replace('\r\n', '\n')
def rep(old, new):
    global html
    if old not in html:
        raise SystemExit('NOT FOUND >>> ' + old[:110])
    html = html.replace(old, new)

# 1. remove MAX MARA (price point too high, per feedback)
i = html.index('  /* MAX MARA — real products */')
j = html.index('  /* NIKE — real products */')
html = html[:i] + html[j:]
rep("  'MAX MARA':{url:'https://us.maxmara.com/'},\n", "")
rep("'FOREVER 21','MAX MARA','73HOURS'", "'FOREVER 21','73HOURS'")
rep("productId:'mm1'", "productId:'ur1'")

# 2. verified-live Nike / Songmont URLs
html = html.replace('https://www.nike.com/w/air-force-1-shoes-5sj3zy', 'https://www.nike.com/w/air-force-1-shoes')
html = html.replace('https://www.nike.com/w/dunk-shoes-5sj3zy', 'https://www.nike.com/w/dunk-shoes')
html = html.replace('https://www.nike.com/t/air-force-1-07-mens-shoes-WrLlWX', 'https://www.nike.com/w/air-force-1-shoes')
html = html.replace('https://songmontofficial.com/products/luna-bag', 'https://songmontofficial.com/collections/all')
html = html.replace('https://songmontofficial.com/collections/bags', 'https://songmontofficial.com/collections/all')

# 3. BUDGETS
rep("const MOODS=[{id:'minimal',en:'Minimal'},{id:'cute',en:'Cute'},{id:'elegant',en:'Elegant'},{id:'sexy',en:'Sexy'}];",
"""const MOODS=[{id:'minimal',en:'Minimal'},{id:'cute',en:'Cute'},{id:'elegant',en:'Elegant'},{id:'sexy',en:'Sexy'}];
const BUDGETS=[{id:'b500',en:'Under ¥500',min:0,max:500},{id:'b1000',en:'¥500–1,000',min:500,max:1000},{id:'b3000',en:'¥1,000–3,000',min:1000,max:3000},{id:'any',en:'No limit',min:0,max:Infinity}];""")

# 4. state — budget field already added to index.html (see earlier patch)

# 5. brief: third question + gate + hint
rep("""      <div class="q-block"><div class="q-head"><span class="q">How do you want to feel?</span></div>
        <div class="chips">${MOODS.map(m=>`<button class="chip ${state.mood===m.id?'sel':''}" data-action="pick-mood" data-id="${m.id}">${m.en}</button>`).join('')}</div></div>
      <button class="btn btn-primary" data-action="build-look" id="buildBtn" style="${state.occasion&&state.mood?'':'opacity:.35;pointer-events:none'}">
        <span class="b-title">✨ Build my look</span><span class="b-sub">score the whole edit · FN-01</span></button>
      <div class="brief-hint">${state.occasion&&state.mood?`Scoring ${CATALOGUE.length-1} pieces across ${Object.keys(BRANDS).length} houses for ${occLabel().toLowerCase()} · ${moodLabel().toLowerCase()}`:'pick one from each — the algorithm will do the rest'}</div>""",
"""      <div class="q-block"><div class="q-head"><span class="q">How do you want to feel?</span></div>
        <div class="chips">${MOODS.map(m=>`<button class="chip ${state.mood===m.id?'sel':''}" data-action="pick-mood" data-id="${m.id}">${m.en}</button>`).join('')}</div></div>
      <div class="q-block"><div class="q-head"><span class="q">What’s your budget?</span></div>
        <div class="chips">${BUDGETS.map(b=>`<button class="chip ${state.budget===b.id?'sel':''}" data-action="pick-budget" data-id="${b.id}">${b.en}</button>`).join('')}</div>
        <div style="font-size:11px;color:var(--gray2);margin-top:8px">FN-05 · Budget matching — pieces that break your range get scored down.</div></div>
      <button class="btn btn-primary" data-action="build-look" id="buildBtn" style="${state.occasion&&state.mood&&state.budget?'':'opacity:.35;pointer-events:none'}">
        <span class="b-title">✨ Build my look</span><span class="b-sub">score the whole edit · FN-01</span></button>
      <div class="brief-hint">${state.occasion&&state.mood&&state.budget?`Scoring ${CATALOGUE.length-1} pieces across ${Object.keys(BRANDS).length} houses for ${occLabel().toLowerCase()} · ${moodLabel().toLowerCase()} · ${budgetLabel().toLowerCase()}`:'pick one from each — the algorithm will do the rest'}</div>""")

# 6. budget label helpers
rep("function occLabel(){const o=OCCASIONS.find(o=>o.id===state.occasion);return o?o.en:'';}",
"""function occLabel(){const o=OCCASIONS.find(o=>o.id===state.occasion);return o?o.en:'';}
function moodLabel(){const m=MOODS.find(m=>m.id===state.mood);return m?m.en:'';}
function budgetEntry(){return BUDGETS.find(b=>b.id===state.budget)||null;}
function budgetLabel(){const b=budgetEntry();return b?b.en:'No limit';}""")

# (remove the now-duplicated old moodLabel definition)
rep("\nfunction moodLabel(){const m=MOODS.find(m=>m.id===state.mood);return m?m.en:'';}\n", "\n")

# 7. budget-aware scoring
rep("""function matchOutfit(){
  const self=getSelf();""",
"""function matchOutfit(){
  const self=getSelf();
  const bEntry=budgetEntry();
  const bMax=bEntry?(bEntry.max||Infinity):Infinity;""")
rep("""      if(c.moods?.length) s += c.moods.includes(state.mood)?30:-25;   // mood mismatch is penalised""",
"""      if(c.moods?.length) s += c.moods.includes(state.mood)?30:-25;   // mood mismatch is penalised
      if(isFinite(bMax)){ if(c.price>bMax) s-=45; else if(c.price>bMax*0.6) s-=12; } // budget fit""")

# 8. results budget line uses the chosen budget
rep("""    <div class="budget-line reveal" style="animation-delay:.5s"><span>FN-05 · Budget matching — styled within ${money(budget)}</span><span class="ok">total ${money(total)} ✓</span></div>""",
"""    <div class="budget-line reveal" style="animation-delay:.5s"><span>FN-05 · Budget matching — “${budgetLabel()}”</span><span class="ok">${total<=budgetMaxNum()?`total ${money(total)} ✓`:`over by ${money(total-budgetMaxNum())} — try ⟳`}</span></div>""")

# 9. budgetMax helper
rep("function budgetEntry(){return BUDGETS.find(b=>b.id===state.budget)||null;}",
"""function budgetEntry(){return BUDGETS.find(b=>b.id===state.budget)||null;}
function budgetMaxNum(){const b=budgetEntry();return b?b.max:Infinity;}""")

# 10. pick-budget handler
rep("    case 'pick-mood': pickBrief('mood',el.dataset.id); break;",
"""    case 'pick-mood': pickBrief('mood',el.dataset.id); break;
    case 'pick-budget': pickBrief('budget',el.dataset.id); break;""")

# 11. pickBrief handles budget
rep('function pickBrief(kind,id){if(kind===\'occ\')state.occasion=id;else state.mood=id;state.picked={};state.altIdx={};state.look=null;renderBrief();}',

# 12. brief build gate includes budget
rep("style=\"${state.occasion&&state.mood?'':'opacity:.35;pointer-events:none'}\">",
    "style=\"${state.occasion&&state.mood&&state.budget?'':'opacity:.35;pointer-events:none'}\">")
rep("${state.occasion&&state.mood?`Scoring", "${state.occasion&&state.mood&&state.budget?`Scoring")

open('index.html','w',encoding='utf-8').write(html)
print('v7 patches applied')

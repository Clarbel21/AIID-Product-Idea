html = open('index.html', encoding='utf-8').read().replace('\r\n', '\n')
fails = []
def rep(old, new):
    global html
    if old not in html:
        fails.append(old[:70]); return
    html = html.replace(old, new)

# A. remove MAX MARA house (5 products) + brand refs
i = html.find('  /* MAX MARA')
if i >= 0:
    j = html.index('  /* NIKE', i)
    html = html[:i] + html[j:]
rep("  'MAX MARA':{url:'https://us.maxmara.com/'},\n", "")
rep("'FOREVER 21','MAX MARA','73HOURS'", "'FOREVER 21','73HOURS'")

# B. verified-live links (replaces dead walls / wrong paths)
html = html.replace('https://www.nike.com/w/air-force-1-shoes-5sj3zy', 'https://www.nike.com/w/air-force-1-shoes')
html = html.replace('https://www.nike.com/w/dunk-shoes-5sj3zy', 'https://www.nike.com/w/dunk-shoes')
html = html.replace('https://www.nike.com/t/air-force-1-07-mens-shoes-WrLlWX', 'https://www.nike.com/w/air-force-1-shoes')
html = html.replace('https://songmontofficial.com/products/luna-bag', 'https://songmontofficial.com/collections/all')
html = html.replace('https://songmontofficial.com/collections/bags', 'https://songmontofficial.com/collections/all')

# C. real photos for mislabelled pieces
rep("price:949, img:'assets/shirt-sky.jpg', cat:'shoes'",
    "price:949, img:'assets/nike-pony.jpg', cat:'shoes'")
rep("{id:'sh4', brand:'73HOURS', name:'Black Stiletto Sandals', price:1090, img:'assets/73h-sole.jpg',",
    "{id:'sh4', brand:'73HOURS', name:'Pointed-Toe Pumps', price:1190, img:'assets/73h-pumps.jpg',")

# D. default product + drop Reebok-photo Nike dupe
rep("productId:'mm1'", "productId:'ur1'")
rep("""  {id:'nk5', brand:'NIKE', name:'Air Force 1 · Triple White', price:799, img:'assets/sneakers.jpg', cat:'shoes', tone:'light', moods:['minimal','elegant'], occs:['office','everyday'], styles:['minimal'], url:'https://www.nike.com/w/air-force-1-shoes', why:'Clean leather, padded collar — white sneakers that go with literally everything.'},
""", "")

# E. BUDGET question + budget-aware scoring
rep("const MOODS=[{id:'minimal',en:'Minimal'},{id:'cute',en:'Cute'},{id:'elegant',en:'Elegant'},{id:'sexy',en:'Sexy'}];",
"""const MOODS=[{id:'minimal',en:'Minimal'},{id:'cute',en:'Cute'},{id:'elegant',en:'Elegant'},{id:'sexy',en:'Sexy'}];
const BUDGETS=[{id:'b500',en:'Under ¥500',min:0,max:500},{id:'b1000',en:'¥500–1,000',min:500,max:1000},{id:'b3000',en:'¥1,000–3,000',min:1000,max:3000},{id:'any',en:'No limit',min:0,max:Infinity}];""")
rep("function matchOutfit(){\n  const self=getSelf();",
"""function matchOutfit(){
  const self=getSelf();
  const bMax=budgetMaxNum();""")
rep("""      if(c.moods?.length) s += c.moods.includes(state.mood)?30:-25;""",
"""      if(c.moods?.length) s += c.moods.includes(state.mood)?30:-25;
      if(isFinite(bMax)){ if(c.price>bMax) s-=45; else if(c.price>bMax*0.6) s-=12; } // budget fit""")
rep("  journeyStep:1, occasion:null, mood:null,", "  journeyStep:1, occasion:null, mood:null, budget:null,")
rep("""      <div class="q-block"><div class="q-head"><span class="q">How do you want to feel?</span></div>
        <div class="chips">${MOODS.map(m=>`<button class="chip ${state.mood===m.id?'sel':''}" data-action="pick-mood" data-id="${m.id}">${m.en}</button>`).join('')}</div></div>
      <button class="btn btn-primary" data-action="build-look" id="buildBtn" style="${state.occasion&&state.mood?'':'opacity:.35;pointer-events:none'}">""",
"""      <div class="q-block"><div class="q-head"><span class="q">How do you want to feel?</span></div>
        <div class="chips">${MOODS.map(m=>`<button class="chip ${state.mood===m.id?'sel':''}" data-action="pick-mood" data-id="${m.id}">${m.en}</button>`).join('')}</div></div>
      <div class="q-block"><div class="q-head"><span class="q">What’s your budget?</span></div>
        <div class="chips">${BUDGETS.map(b=>`<button class="chip ${state.budget===b.id?'sel':''}" data-action="pick-budget" data-id="${b.id}">${b.en}</button>`).join('')}
        <div style="font-size:11px;color:var(--gray2);margin-top:8px">FN-05 · Budget matching — pieces that break your range get scored down.</div></div>
      <button class="btn btn-primary" data-action="build-look" id="buildBtn" style="${state.occasion&&state.mood&&state.budget?'':'opacity:.35;pointer-events:none'}">""")
rep("${state.occasion&&state.mood?`Scoring", "${state.occasion&&state.mood&&state.budget?`Scoring")
rep("    case 'pick-mood': pickBrief('mood',el.dataset.id); break;",
"""    case 'pick-mood': pickBrief('mood',el.dataset.id); break;
    case 'pick-budget': pickBrief('budget',el.dataset.id); break;""")
rep("""function pickBrief(kind,id){if(kind==='occ')state.occasion=id;else state.mood=id;""",
"""function pickBrief(kind,id){if(kind==='budget')state.budget=id;else if(kind==='occ')state.occasion=id;else state.mood=id;""")

# F. budget helpers + budget-aware results line + foot meta
rep("function occLabel(){const o=OCCASIONS.find(o=>o.id===state.occasion);return o?o.en:'';}",
"""function occLabel(){const o=OCCASIONS.find(o=>o.id===state.occasion);return o?o.en:'';}
function budgetEntry(){return BUDGETS.find(b=>b.id===state.budget)||null;}
function budgetMaxNum(){const b=budgetEntry();return (b&&isFinite(b.max))?b.max:Infinity;}
function budgetLabel(){const b=budgetEntry();return b?b.en:'No limit';}""")
rep("""    <div class="budget-line reveal" style="animation-delay:.5s"><span>FN-05 · Budget matching — styled within ${money(budget)}</span><span class="ok">total ${money(total)} ✓</span></div>""",
"""    <div class="budget-line reveal" style="animation-delay:.5s"><span>FN-05 · Budget matching — “${budgetLabel()}”</span><span class="ok">${total<=budgetMaxNum()?`total ${money(total)} ✓`:`over by ${money(total-budgetMaxNum())} — try ⟳`}</span></div>""")

open('index.html','w',encoding='utf-8').write(html)
print('FAILS:', len(fails))
for f in fails: print('  MISSING:', f)

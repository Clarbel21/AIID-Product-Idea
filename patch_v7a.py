html = open('index.html', encoding='utf-8').read()
fails = []
def rep(old, new):
    global html
    if old not in html:
        fails.append(old[:60]); return
    html = html.replace(old, new)

# 1. weighted scoring — replaces the ad-hoc penalty block inside matchOutfit
old_score = """      let s=50;
      if(c.moods?.length) s += c.moods.includes(state.mood)?30:-25;
      if(c.occs?.length)   s += c.occs.includes(state.occasion)?18:-12;
      s+=toneScore(self.tone,c.tone);
      if(!used.includes(c.brand)) s+=8;
      if(c.price>self.price*4) s-=8;
      s+=(c.id.length%5);
      if(s>bestS){bestS=s;best=c;}"""
new_score = """      const d = scoreDimensions(self, c, slot);
      let s = d.style*0.30 + d.colour*0.25 + d.silhouette*0.20 + d.occasion*0.15 + d.budget*0.10;
      if(!used.includes(c.brand)) s += 6; // cross-house bonus
      if(c.moods?.length && !c.moods.includes(state.mood)) s -= 18;
      if(c.price > self.price*4) s -= 8;
      s += (c.id.length % 5);
      if(s > bestS){ bestS = s; best = c; bestDims = d; }"""
rep(old_score, new_score)

# 1b. declare bestDims + scoreDimensions + budget helpers
rep("function matchOutfit(){\n  const self=getSelf();",
"""function styleFamily(s){return {minimal:'quiet',classic:'quiet',elegant:'refined',sexy:'expressive',romantic:'expressive',cute:'playful',sporty:'sport',casual:'sport',bold:'expressive'}[s]||s;}
function colourHarmony(a,b){
  const neutral={light:1,dark:1}, base={light:0,dark:1,warm:2,cool:3};
  if(neutral[a]&&neutral[b]) return 88;
  if(a===b) return 82;
  if((a==='warm'&&b==='cool')||(a==='cool'&&b==='warm')) return 55;
  return 78;
}
function silBalance(a,b){
  const soft=['flowy','oversized','relaxed'], structured=['cropped','fitted','structured','heeled'];
  const fa=soft.includes(a)?'soft':(structured.includes(a)?'struct':'mid');
  const fb=soft.includes(b)?'soft':(structured.includes(b)?'struct':'mid');
  if(fa!==fb) return 96; // balance contrast
  if(fa==='mid'&&fb==='mid') return 78;
  return 72;
}
function scoreDimensions(a, c, slot){
  const target = styleFamily(state.mood==='minimal'?'minimal':state.mood==='elegant'?'elegant':state.mood==='cute'?'romantic':state.mood==='sexy'?'expressive':'casual');
  const cStyle = styleFamily(c.style || 'minimal');
  let style = (cStyle===target) ? 96 : 74;
  const colour = colourHarmony(a.colourFamily||'light', c.colourFamily||'light');
  const silhouette = silBalance(a.silhouette||'fitted', c.silhouette||'relaxed');
  let occasion = 60;
  if(c.occs && c.occs.includes(state.occasion)) occasion = 96;
  else if((c.occs||[]).some(o => (OCCASIONS.find(x=>x.id===state.occasion)||{adj:[]}).adj && false)) occasion = 75;
  const bEntry = budgetEntry();
  const bMax = (bEntry && isFinite(bEntry.max)) ? bEntry.max : Infinity;
  let budget = isFinite(bMax) ? (c.price<=bMax ? Math.max(55, 100 - Math.round(35*(c.price/bMax))) : 35) : 85;
  return {style: Math.min(99,style+2), colour: Math.min(99,colour+2), silhouette: Math.min(99,silhouette+2), occasion: Math.min(99,occasion+2), budget};
}
function matchOutfit(){
  const self=getSelf();
  const bEntry=budgetEntry();
  const bMax=(bEntry&&isFinite(bEntry.max))?bEntry.max:Infinity;""")

# 2. brand filter chips row in results (before budget-line)
rep('    <div class="budget-line reveal" style="animation-delay:.5s">',
"""    <div class="reveal" style="animation-delay:.45s;display:flex;gap:8px;flex-wrap:wrap;margin:4px 0 14px">
      ${['any','same','budget'].map(f=>`<button class="lm ${state.brandFilter===f?'lm-on':''}" data-action="brand-filter" data-f="${f}" style="cursor:pointer;${state.brandFilter===f?'border-color:var(--blush-d);color:var(--blush-d)':''}">${f==='any'?'ANY BRAND':f==='same'?'SAME BRAND':'UNDER BUDGET'}</button>`).join('')}
    </div>
    <div class="budget-line reveal" style="animation-delay:.5s">""")

# 3. brand-filter handler + state
rep("  journeyStep:1, occasion:null, mood:null, budget:null,",
    "  journeyStep:1, occasion:null, mood:null, budget:null, brandFilter:'any',")
rep("    case 'pick-budget': pickBrief('budget',el.dataset.id); break;",
"""    case 'pick-budget': pickBrief('budget',el.dataset.id); break;
    case 'brand-filter': state.brandFilter = el.dataset.f; renderResults(); break;""")

# 3b. apply brand filter inside matchOutfit candidate loop
rep("      if(c.id===self.id || c.cat!==slot || chosen.includes(c)) continue;",
"""      if(c.id===self.id || c.cat!==slot || chosen.includes(c)) continue;
      if(state.brandFilter==='same' && c.brand!==self.brand) continue;""")

open('index.html','w',encoding='utf-8').write(html)
print('applied with', len(fails), 'skipped')
for f in fails: print('  MISSING:', f)

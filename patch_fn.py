html = open('index.html', encoding='utf-8').read()
start = html.index('function matchOutfit(){')
# the next top-level 'function ' after matchOutfit marks its end
nxt = html.index('\nfunction ', start + 10)
old_fn = html[start:nxt]
new_fn = '''function matchOutfit(){
  const self = getSelf();
  const bEntry = budgetEntry();
  const bMax = (bEntry && isFinite(bEntry.max)) ? bEntry.max : Infinity;
  const needed = (SLOTS_FOR[self.cat] || []).filter(s => state.slots.includes(s));
  const chosen = [];
  const used = [self.brand];
  let spent = self.price;
  for (const slot of needed) {
    let best = null, bestS = -1, bestDims = null;
    for (const c of CATALOGUE) {
      if (c.id === self.id || c.cat !== slot || chosen.includes(c)) continue;
      if (state.brandFilter === 'same' && c.brand !== self.brand) continue;
      const d = scoreDimensions(self, c);
      let s = d.total;
      if (!used.includes(c.brand)) s += 6;
      if (isFinite(bMax) && spent + c.price > bMax) s -= 40;      // budget steering
      s += (c.id.length % 5);
      if (s > bestS) { bestS = s; best = c; }
    }
    if (!best) continue;
    chosen.push(best); used.push(best.brand); spent += best.price;
  }
  state.lastSpend = spent;
  return [{ slot: 'self', item: self, score: 100, dims: null }, ...chosen.map(c => ({ slot: c.cat, item: c, score: Math.min(99, Math.round(60 + 0.4 * scoreDimensions(self, c).total + 0)) }))];
}
'''
# keep per-item scores stable: reuse scoreDimensions total for display
html = html[:start] + new_fn + html[nxt:]
# per-item display score = scoreDimensions(style+colour+...)? use the dimension avg — compute in scoreDimensions already? simplest: display Math.round(d.total) via scoreDimensions
open('index.html','w',encoding='utf-8').write(html)
print('matchOutfit replaced; old fn len', len(old_fn))

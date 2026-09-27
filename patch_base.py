html = open('index.html', encoding='utf-8').read().replace('\r\n', '\n')
def rep(old, new):
    global html
    if old not in html:
        raise SystemExit('NOT FOUND >>> ' + old[:100])
    html = html.replace(old, new)

# 1. 73Hours: drop the sole close-up shot, fix mislabelled photos
rep("{id:'sh4', brand:'73HOURS', name:'Black Stiletto Sandals', price:1090, img:'assets/73h-sole.jpg',",
    "{id:'sh4', brand:'73HOURS', name:'Pointed-Toe Pumps', price:1190, img:'assets/73h-pumps.jpg',")
rep("{id:'sh5', brand:'73HOURS', name:'Pointed-Toe Pumps · Trio', price:1190, img:'assets/shirt-sky.jpg',",
    "{id:'sh5', brand:'73HOURS', name:'Lace Kitten Heel · Nude', price:890, img:'assets/73h-lace.jpg',")

# 2. Nike: real AF1 photos (was a tank photo / a Reebok heel)
rep("price:949, img:'assets/shirt-sky.jpg', cat:'shoes'",
    "price:949, img:'assets/nike-pony.jpg', cat:'shoes'")
rep("{id:'nk5', brand:'NIKE', name:'Air Force 1 · Triple White', price:799, img:'assets/sneakers.jpg',",
    "{id:'nk5', brand:'NIKE', name:\"Air Force 1 '07 LV8 · White\", price:849, img:'assets/nike-af1-studio.png',")

# 3. remove the Sporty & Rich entry (user: not a real product)
i = html.index('  /* SPORTY & RICH')
end = html.index('];', i)
html = html[:i] + '];' + html[end+2:]
rep("  'SPORTY & RICH':{url:'https://www.sportyandrich.com/'},\n", "")
rep("const BRAND_ORDER = ['SPORTY & RICH','URBAN REVIVO',", "const BRAND_ORDER = ['URBAN REVIVO',")
rep("productId:'sr-tank'", "productId:'mm1'")

# 4. no unverified returns/shipping claims (30-day returns only where the house offers it)
rep("<span>\u21a9 30-day returns on the house</span>",
    "<span>\u21a9 Returns &amp; shipping per the house\u2019s own policy</span>")

# 5. sizes: hide the selector for one-size categories (jewelry, bags)
rep("  const st=Math.round(p.rating||4.8);",
    """  const sizes=(p.sizes||['One size']);
  const showSizes=!((p.cat==='accessory'||p.cat==='bag')||(sizes.length===1&&sizes[0]==='One size'));
  if(!showSizes) state.sizePDP=sizes[0]||'One size';
  const sizesHTML=showSizes?`
    <div class="opt-label">Size <span class="val">Size guide</span></div>
    <div class="sizes">${sizes.map(s=>`<button class="size-chip ${s===state.sizePDP?'sel':''}" data-action="size" data-s="${s}">${s}</button>`).join('')}</div>`:'';""")
rep("""    <div class="opt-label">Size <span class="val">Size guide</span></div>
    <div class="sizes">${(p.sizes||self.sizes).map(s=>`<button class="size-chip ${s===state.sizePDP?'sel':''}" data-action="size" data-s="${s}">${s}</button>`).join('')}</div>""",
    "    ${sizesHTML}")

# 6. wishlist panel markup exists in the DOM
rep("<!-- toast / guide -->",
"""<!-- wishlist -->
<div class="scrim" id="wlScrim" data-action="close-wl"></div>
<aside class="wish-panel" id="wishPanel" aria-label="Wishlist">
  <div class="wp-head"><h2>WISHLIST</h2><span class="ml" id="wlCountLbl"></span><button class="dr-close" data-action="close-wl" title="Close">✕</button></div>
  <div class="wp-body" id="wlBody"></div>
  <div class="wp-foot">Saved on this device · tap ♡ on any piece to add</div>
</aside>

<!-- toast / guide -->""")

# 7. filled-heart styling + pop animation + hero-fav state
rep(".wish.on{color:#C04A5A}",
    ".wish.on{color:#C04A5A;background:var(--blush-t)}\n.hero-fav.on{color:#C04A5A;background:var(--blush-t)}\n@keyframes wishPop{50%{transform:scale(1.3)}}\n.wish.on,.hero-fav.on{animation:wishPop .3s}")

# 8. PDP masthead heart opens the wishlist + badge
rep('<button class="hicon" data-action="noop" title="Cart">🛍<span class="hcount hidden" id="cartBadge">0</span></button>',
    '<button class="hicon" data-action="open-wl" title="Wishlist">♡<span class="hcount hidden" id="wishCountPDP">0</span></button>\n          <button class="hicon" data-action="noop" title="Cart">🛍<span class="hcount hidden" id="cartBadge">0</span></button>')

# 9. wishlist count badge on both mastheads
rep("""function renderWishCount(){
  const b=$('#wishCount');if(!b)return;
  b.textContent=state.wishlist.length;
  b.classList.toggle('hidden',state.wishlist.length===0);
}""",
"""function renderWishCount(){
  ['wishCount','wishCountPDP'].forEach(id=>{
    const b=document.getElementById(id);if(!b)return;
    b.textContent=state.wishlist.length;
    b.classList.toggle('hidden',state.wishlist.length===0);
  });
}""")

# 10. clean open/close wishlist (panel now exists in the DOM)
rep("""function openWl(){renderWishPanel();$('#wlScrim')&&0;$('#wishPanel').classList.add('on');document.body.classList.add('locked');
  if(!document.getElementById('wlScrim')){const s=document.createElement('div');s.className='scrim';s.id='wlScrim';s.dataset.action='close-wl';document.body.appendChild(s);requestAnimationFrame(()=>s.classList.add('on'));}
}
function closeWl(){const p=$('#wishPanel');if(p)p.classList.remove('on');const s=document.getElementById('wlScrim');if(s)s.classList.remove('on');document.body.classList.remove('locked');}
function renderWishPanel(){
  let head=$('#wlHead');
  if(!head){
    const panel=$('#wishPanel');
    panel.innerHTML=`<div class="wp-head" id="wlHead"><h2>WISHLIST</h2><span class="ml" id="wlCountLbl"></span><button class="dr-close" data-action="close-wl" title="Close">✕</button></div><div class="wp-body" id="wlBody"></div><div class="wp-foot">Saved on this device · tap ♡ on any piece to add</div>`;
  }
  $('#wlCountLbl').textContent=state.wishlist.length+(state.wishlist.length===1?' piece saved':' pieces saved');""",
"""function openWl(){renderWishPanel();$('#wlScrim').classList.add('on');$('#wishPanel').classList.add('on');document.body.classList.add('locked');}
function closeWl(){$('#wlScrim').classList.remove('on');$('#wishPanel').classList.remove('on');if(state.view!=='pdp')document.body.classList.remove('locked');}
function renderWishPanel(){
  $('#wlCountLbl').textContent=state.wishlist.length+(state.wishlist.length===1?' piece saved':' pieces saved');""")

# 11. guide modal house list
rep("Max Mara, Pomelo, Brandy Melville, 73Hours, Nike, Adidas, Charles &amp; Keith and Swarovski.",
    "Urban Revivo, Zara, Forever 21, Max Mara, 73Hours, Nike, Adidas, JW PEI, Songmont, DeMellier and Swarovski.")

open('index.html','w',encoding='utf-8').write(html)
print('all patches applied')

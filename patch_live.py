html = open('index.html', encoding='utf-8').read().replace('\r\n', '\n')
def rep(old, new):
    global html
    if old not in html:
        raise SystemExit('NOT FOUND >>> ' + old[:90])
    html = html.replace(old, new)

# A. JW PEI: replace all 5 entries with live-verified products (title/price/image from jwpei.com)
i = html.index('  /* JW PEI — real products */')
j = html.index('  /* SONGMONT — real products */')
html = html[:i] + """  /* JW PEI — live catalogue data */
  {id:'jp1', brand:'JW PEI', name:'Hana Medium Tote · Claret', price:1019, img:'assets/jwp1.jpg', cat:'bag', tone:'warm', moods:['cute','elegant'], occs:['office','date'], styles:['minimal'], url:'https://www.jwpei.com/products/hana-medium-tote-bag-claret', why:'Claret grained leather with gold feet — a quiet statement for work and after.'},
  {id:'jp2', brand:'JW PEI', name:'Noor Top Handle · Elephant Grey', price:719, img:'assets/jwpei2.jpg', cat:'bag', tone:'cool', moods:['minimal','sexy'], occs:['everyday','office'], styles:['minimal'], url:'https://www.jwpei.com/products/noor-top-handle-bag-elephant-gray', why:'Sculpted grey top handle — the quiet one that sharpens neutrals.'},
  {id:'jp3', brand:'JW PEI', name:'Hana Mini Tote · Navy', price:719, img:'assets/jwp3.jpg', cat:'bag', tone:'cool', moods:['minimal','elegant'], occs:['office','everyday'], styles:['minimal'], url:'https://www.jwpei.com/products/hana-mini-tote-bag-navy-blue', why:'A neat navy mini — hands-free structure for every day.'},
  {id:'jp4', brand:'JW PEI', name:'Cleo Box Bag · Black Croc', price:789, img:'assets/jwp4.jpg', cat:'bag', tone:'dark', moods:['elegant','sexy'], occs:['date','party'], styles:['classic'], url:'https://www.jwpei.com/products/cleo-box-shape-top-handle-bag-black-croc', why:'Black croc-emboss box bag — the evening anchor of the edit.'},
  {id:'jp5', brand:'JW PEI', name:'Hana Medium Tote · Navy', price:1019, img:'assets/jwp5.jpg', cat:'bag', tone:'cool', moods:['cute','minimal'], occs:['everyday'], styles:['casual'], url:'https://www.jwpei.com/products/hana-medium-tote-bag-navy-blue', why:'The navy Hana — soft structure for errand days and brunch.'},
""" + html[j:]

# B. budget chips sized to the real catalogue
rep("const BUDGETS=[{id:'b500',en:'Under ¥500',min:0,max:500},{id:'b1000',en:'¥500–1,000',min:500,max:1000},{id:'b3000',en:'¥1,000–3,000',min:1000,max:3000},{id:'any',en:'No limit',min:0,max:Infinity}];",
"""const BUDGETS=[{id:'b2500',en:'Under ¥2,500',min:0,max:2500},{id:'b3500',en:'¥2,500–3,500',min:2500,max:3500},{id:'b5000',en:'¥3,500–5,000',min:3500,max:5000},{id:'any',en:'No limit',min:0,max:Infinity}];""")

# C. budget-steered scoring: penalise pieces that push the running total past the range
rep("""      if(isFinite(bMax)){ if(c.price>bMax) s-=45; else if(c.price>bMax*0.6) s-=12; } // budget fit""",
"""      if(isFinite(bMax)){
        const spent=self.price+chosen.reduce((t,x)=>t+x.item.price,0);
        const projected=spent+c.price;
        if(projected>bMax) s-=30+Math.min(45,Math.round((projected-bMax)/40)*5); // keeps the look inside range
      }""")

open('index.html','w',encoding='utf-8').write(html)
print('JW PEI live data + budget chips + steering applied')

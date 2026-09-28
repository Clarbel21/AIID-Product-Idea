html = open('index.html', encoding='utf-8').read()
fails = []
def rep(old, new):
    global html
    if old not in html:
        fails.append(old[:60]); return
    html = html.replace(old, new)

# A. replace the NIKE section with the 6 real products
i = html.find('  /* NIKE — real products */')
j = html.find('  /* ADIDAS — real products */')
if i < 0 or j < 0:
    raise SystemExit('nike block anchors missing')
nike_new = """  /* NIKE — real products · nike.com */
  {id:'nk-vom5-mah', retailer:'NIKE', name:'Zoom Vomero 5 · Mahogany', category:'shoes', price:1229, img:'assets/nike-vomero5-olive.jpg', url:'https://www.nike.com/t/zoom-vomero-5-womens-shoe-with-reflective-accents-81TPKW/HQ0458-202', colourFamily:'warm', colourName:'Mahogany', style:'sporty', silhouette:'sneaker', occasions:['casual','office'], material:'Mesh & leather', moods:['minimal','elegant'], tags:['vomero'], why:'The cult Vomero in mahogany — vintage runner shape, modern cushioning.'},
  {id:'nk-vom5-wht', retailer:'NIKE', name:'Zoom Vomero 5 · White', category:'shoes', price:1229, img:'assets/nike-vomero5-white.jpg', url:'https://www.nike.com/t/zoom-vomero-5-womens-shoes-81TPKW/IV4311-100', colourFamily:'light', colourName:'Photon dust', style:'minimal', silhouette:'sneaker', occasions:['casual','office'], material:'Mesh & leather', moods:['minimal','cute'], tags:['vomero'], why:'All-white Vomero — the cleanest possible base for any cropped look.'},
  {id:'nk-vic4', retailer:'NIKE', name:'Victory Pro 4 Golf Shoes', category:'shoes', price:949, img:'assets/nike-victory4-golf.jpg', url:'https://www.nike.com/t/victory-pro-4-golf-shoes-N2eIegYv/FZ7611-104', colourFamily:'light', colourName:'Sail/olive', style:'sporty', silhouette:'sneaker', occasions:['casual','office'], material:'Leather', moods:['minimal'], tags:['golf'], why:'Golf-core is a thing — crisp leather with a spiked outsole.'},
  {id:'nk-am95', retailer:'NIKE', name:'Air Max 95 Big Bubble · WNBA', category:'shoes', price:1099, img:'assets/nike-am95-wnba.jpg', url:'https://www.nike.com/t/air-max-95-big-bubble-wnba-all-star-weekend-womens-shoes-C8qkmu3G/IV5831-001', colourFamily:'light', colourName:'Photon dust/multi', style:'sporty', silhouette:'sneaker', occasions:['casual','party'], material:'Mesh & leather', moods:['cute','sexy'], tags:['air max'], why:'Big-bubble Air Max — a chunky, confident counterpoint to soft tailoring.'},
  {id:'nk-p6000', retailer:'NIKE', name:'P-6000', category:'shoes', price:829, img:'assets/nike-p6000.jpg', url:'https://www.nike.com/t/p-6000-womens-shoes-SGxVgg/BV1021-022', colourFamily:'light', colourName:'Metallic silver', style:'sporty', silhouette:'sneaker', occasions:['casual','office'], material:'Leather & textile', moods:['minimal','cute'], tags:['p-6000'], why:'Y2K P-6000 lines — the retro-future sneaker that matches everything metallic.'},
  {id:'nk-v5rnr', retailer:'NIKE', name:'V5 RNR · White', category:'shoes', price:689, img:'assets/nike-v5rnr.jpg', url:'https://www.nike.com/t/v5-rnr-womens-shoes-4Lts7n/IO7801-101', colourFamily:'light', colourName:'White', style:'sporty', silhouette:'sneaker', occasions:['casual'], material:'Textile', moods:['cute','minimal'], tags:['v5 rnr'], why:'V5 RNR — a fresh white runner for easy, everyday fits.'},
"""
html = html[:i] + nike_new + html[j:]

# B. replace the ADIDAS section with the 6 real products
i = html.find('  /* ADIDAS — real products */')
j = html.find('  /* JW PEI', i)
if i < 0 or j < 0:
    raise SystemExit('adidas block anchors missing')
ad_new = """  /* ADIDAS — real products · adidas.com */
  {id:'ad-g7-black', retailer:'ADIDAS', name:'Galaxy 7 Running Shoes · Black', category:'shoes', price:369, img:'assets/adidas-galaxy7-white.jpg', url:'https://www.adidas.com/us/galaxy-7-running-shoes/ID8765.html', colourFamily:'dark', colourName:'Black', style:'sporty', silhouette:'sneaker', occasions:['casual','office'], material:'Textile', moods:['minimal'], tags:['galaxy 7'], why:'The Galaxy 7 on sale — a black everyday runner that disappears into any look.'},
  {id:'ad-sxl', retailer:'ADIDAS', name:'Samba XLG · White', category:'shoes', price:399, img:'assets/adidas-samba-xlg.jpg', url:'https://www.adidas.com/us/samba-xlg-shoes/IE1377.html', colourFamily:'light', colourName:'White', style:'sporty', silhouette:'sneaker', occasions:['casual','date'], material:'Leather', moods:['cute','minimal'], tags:['samba xlg'], why:'The XLG Samba in white — 50% off and the easiest wear in the edit.'},
  {id:'ad-vlc', retailer:'ADIDAS', name:'VL Court Bold · Grey', category:'shoes', price:399, img:'assets/adidas-vl-court.jpg', url:'https://www.adidas.com/us/vl-court-bold-shoes/IF9784.html', colourFamily:'light', colourName:'Grey', style:'casual', silhouette:'sneaker', occasions:['casual','office'], material:'Leather', moods:['minimal','elegant'], tags:['vl court'], why:'A grey VL Court — 30% off, quietly matches everything neutral.'},
  {id:'ad-gazb', retailer:'ADIDAS', name:'Gazelle Bold · Black', category:'shoes', price:519, img:'assets/adidas-gazelle-bold.jpg', url:'https://www.adidas.com/us/gazelle-bold-shoes/HQ6912.html', colourFamily:'dark', colourName:'Black', style:'classic', silhouette:'sneaker', occasions:['date','party','office'], material:'Leather', moods:['elegant','sexy'], tags:['gazelle bold'], why:'The Gazelle Bold platform — black leather, 40% off, goes with everything.'},
  {id:'ad-stl', retailer:'ADIDAS', name:'Stella McCartney Dropset 4 · Beige', category:'shoes', price:1299, img:'assets/adidas-stella-dropset4.jpg', cat2:'shoes', tone:'light', url:'https://www.adidas.com/us/adidas-by-stella-mccartney-dropset-4-sneaker/KJ6183.html', colourFamily:'light', colourName:'Beige', style:'minimal', silhouette:'sneaker', occasions:['office','casual'], material:'Recycled textile', moods:['minimal','elegant'], tags:['stella'], why:'Stella McCartney training shoe — the designer tier of the edit.'},
  {id:'ad-dr4', retailer:'ADIDAS', name:'Dropset 4 · Pink', category:'shoes', price:1039, img:'assets/adidas-dropset4-power.jpg', url:'https://www.adidas.com/us/dropset-4-power-training-shoes/KJ0421.html', colourFamily:'light', colourName:'Pink', style:'sporty', silhouette:'sneaker', occasions:['casual'], material:'Textile', moods:['cute','sexy'], tags:['dropset'], why:'Pink Dropset 4 — training shoes that make the athleisure case.'},
"""
html = html[:i] + ad_new + html[j:]

open('index.html','w',encoding='utf-8').write(html)
print('NIKE + ADIDAS sections rebuilt with real products')

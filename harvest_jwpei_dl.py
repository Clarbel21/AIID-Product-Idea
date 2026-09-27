import json, urllib.request, ssl
ctx = ssl.create_default_context(); ctx.check_hostname = False; ctx.verify_mode = ssl.CERT_NONE
UA = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/126 Safari/537.36'}
def get(url):
    req = urllib.request.Request(url, headers=UA)
    return urllib.request.urlopen(req, timeout=30, context=ctx).read()
def get_json(url):
    return json.loads(get(url).decode())

d = get_json('https://www.jwpei.com/collections/shop-all/products.json?limit=60')
byp = {p['handle']: p for p in d['products']}
picks = ['cleo-box-shape-top-handle-bag-brown','hana-medium-tote-bag-claret','noor-top-handle-bag-elephant-gray','hana-mini-tote-bag-navy-blue','cleo-box-shape-top-handle-bag-black-croc']
for i, hdl in enumerate(picks, 1):
    p = byp[hdl]
    v = p['variants'][0]
    img = p['images'][0]['src']
    fn = f'assets/jwp{i}.jpg'
    open(fn, 'wb').write(get(img))
    print(f"jwp{i}: {p['title']} | ${v['price']} | saved {fn}")

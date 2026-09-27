import json, urllib.request, ssl
ctx = ssl.create_default_context(); ctx.check_hostname = False; ctx.verify_mode = ssl.CERT_NONE
UA = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/126 Safari/537.36'}
def get_json(url):
    req = urllib.request.Request(url, headers={**UA, 'Accept': 'application/json'})
    return json.loads(urllib.request.urlopen(req, timeout=25, context=ctx).read().decode())

# JW PEI: live in-stock bags straight from the shop-all collection JSON
try:
    d = get_json('https://www.jwpei.com/collections/shop-all/products.json?limit=60')
    bags = [p for p in d['products'] if p['product_type'] == 'Bags' or 'bag' in p['title'].lower() or 'tote' in p['title'].lower()]
    print('JW PEI live products:', len(d['products']), '| bags:', len(bags))
    for p in bags[:10]:
        v = p['variants'][0]
        img = p['images'][0]['src'] if p['images'] else None
        print(f"  - {p['title']} | ${v['price']} | {p['handle']} | img:{'yes' if img else 'no'} | avail:{v['available']}")
except Exception as e:
    print('JW PEI collection failed:', e)

import json, urllib.request, ssl, re
ctx = ssl.create_default_context(); ctx.check_hostname = False; ctx.verify_mode = ssl.CERT_NONE
UA = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/126 Safari/537.36'}
def get(url):
    req = urllib.request.Request(url, headers=UA)
    return urllib.request.urlopen(req, timeout=30, context=ctx).read()
def get_json(url):
    return json.loads(get(url).decode())

# 1. Shopify stores: live title/price/image/availability per handle
SHOP = {
 'UR': 'https://global.urbanrevivo.com',
 'DEM': 'https://demellierlondon.com',
 'JWP': 'https://www.jwpei.com',
}
handles = {
 'UR': ['button-front-peplum-off-shoulder-sleeveless-cotton-shirt-uwg860127',
        'oversized-wrap-front-thin-stretch-cotton-shirt-uwj260107',
        'tailored-pleated-shirts-uwm260016',
        'cutout-fitted-mock-neck-sleeveless-cotton-blouse-uyv260074',
        'textured-striped-v-neck-short-sleeve-cotton-shirt-uyv260075',
        'ruffle-midi-fishtail-skirt-uwj540010',
        'pinstripe-weave-high-waist-buttoned-wrap-overlay-draped-panel-asymmetric-hemline-skirt-uwj560048',
        'midi-denim-skirt-uwm840026'],
 'DEM': ['the-small-hudson-dark-green-small-grain',
         'the-brooklyn-warm-brown-small-grain',
         'the-midi-stockholm-midnight-blue-fine-grain',
         'the-florence-crossbody-bordeaux-fine-grain',
         'the-large-siena-bucket-hazel-suede'],
 'JWP': ['cleo-box-shape-top-handle-bag-brown',
         'noor-top-handle-bag-pink-croc',
         'hana-mini-tote-bag-navy-blue',
         'yara-shoulder-bag-dark-brown',
         'nala-woven-texture-wide-tote-bag-navy-blue',
         'tulip-shape-shoulder-bag-forest-green',
         'hana-medium-tote-bag-claret',
         'hana-large-tote-bag-dark-brown',
         'cleo-box-shape-top-handle-bag-black-croc'],
}
out = {}
for brand, base in SHOP.items():
    for h in handles[brand]:
        try:
            d = get_json(f'{base}/products/{h}.json')['product']
            v = d['variants'][0]
            img = d['images'][0]['src'] if d['images'] else ''
            if img.startswith('//'): img = 'https:' + img
            out[f'{brand}:{h}'] = {'title': d['title'], 'price': v['price'],
                                   'currency': v.get('price_currency',''), 'avail': v['available'],
                                   'img': img, 'url': f'{base}/products/{h}'}
            print('OK ', brand, h[:40], '|', v['price'], '| avail', v['available'])
        except Exception as e:
            print('FAIL', brand, h[:40], str(e)[:50])
json.dump(out, open('sync_shopify.json','w'), indent=1)
print('shopify synced:', len(out))

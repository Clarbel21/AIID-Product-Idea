import json, urllib.request, ssl
ctx = ssl.create_default_context(); ctx.check_hostname = False; ctx.verify_mode = ssl.CERT_NONE
UA = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/126 Safari/537.36'}

def get(url):
    req = urllib.request.Request(url, headers=UA)
    return urllib.request.urlopen(req, timeout=40, context=ctx).read()

def get_json(url):
    return json.loads(get(url).decode())

SHOP = {
    'UR':  ('https://global.urbanrevivo.com', [
        'button-front-peplum-off-shoulder-sleeveless-cotton-shirt-uwg860127',
        'oversized-wrap-front-thin-stretch-cotton-shirt-uwj260107',
        'tailored-pleated-shirts-uwm260016',
        'cutout-fitted-mock-neck-sleeveless-cotton-blouse-uyv260074',
        'textured-striped-v-neck-short-sleeve-cotton-shirt-uyv260075',
        'ruffle-midi-fishtail-skirt-uwj540010',
        'pinstripe-weave-high-waist-buttoned-wrap-overlay-draped-panel-asymmetric-hemline-skirt-uwj560048',
        'midi-denim-skirt-uwm840026']),
    'DEM': ('https://demellierlondon.com', [
        'the-small-hudson-dark-green-small-grain',
        'the-brooklyn-warm-brown-small-grain',
        'the-midi-stockholm-midnight-blue-fine-grain',
        'the-florence-crossbody-bordeaux-fine-grain',
        'the-large-siena-bucket-hazel-suede']),
    'JWP': ('https://www.jwpei.com', [
        'cleo-box-shape-top-handle-bag-brown',
        'noor-top-handle-bag-pink-croc',
        'hana-mini-tote-bag-navy-blue',
        'nala-woven-texture-wide-tote-bag-navy-blue',
        'tulip-shape-shoulder-bag-forest-green',
        'hana-medium-tote-bag-claret']),
}

out = {}
for brand, (base, hs) in SHOP.items():
    for h in hs:
        try:
            d = get_json(base + '/products/' + h + '.json')['product']
            v = d['variants'][0]
            img = (d['images'][0]['src'] if d['images'] else '')
            if img.startswith('//'):
                img = 'https:' + img
            avail = v.get('available', True)
            out[brand + ':' + h] = {
                'title': d['title'],
                'price': v['price'],
                'currency': v.get('price_currency', 'USD'),
                'available': avail,
                'img': img,
            }
            print('OK ', brand, h[:44], '|', v['price'], v.get('price_currency', 'USD'), '| avail', avail)
        except Exception as e:
            print('FAIL', brand, h[:44], str(e)[:60])
json.dump(out, open('sync_result.json', 'w'), indent=1)
print('total:', len(out))

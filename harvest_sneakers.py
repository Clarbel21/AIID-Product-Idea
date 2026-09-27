import urllib.request, ssl, re, json
ctx = ssl.create_default_context(); ctx.check_hostname = False; ctx.verify_mode = ssl.CERT_NONE
UA = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36',
      'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
      'Accept-Language': 'en-US,en;q=0.9'}
def page(url):
    req = urllib.request.Request(url, headers=UA)
    return urllib.request.urlopen(req, timeout=30, context=ctx).read().decode('utf-8', 'ignore')

targets = {
 'NIKE_AF1': 'https://www.nike.com/t/air-force-1-07-mens-shoes-WrLlWX',
 'NIKE_AF1_W': 'https://www.nike.com/t/air-force-1-07-womens-shoes-NMmm1B',
 'ADIDAS_SAMBA': 'https://www.adidas.com/us/samba-og-shoes',
}
for key, url in targets.items():
    try:
        h = page(url)
        ld = re.findall(r'<script type="application/ld\+json"[^>]*>(.*?)</script>', h, re.S)
        found = None
        for block in ld:
            try:
                j = json.loads(block)
                items = j if isinstance(j, list) else [j]
                for it in items:
                    if it.get('@type') == 'Product':
                        found = it
            except Exception:
                pass
        og = re.search(r'property="og:image" content="([^"]+)"', h)
        print('===', key, '| html len', len(h))
        if found:
            offers = found.get('offers') or {}
            print('  name:', found.get('name'))
            print('  image:', (found.get('image') or ['?'])[0] if isinstance(found.get('image'), list) else str(found.get('image'))[:100])
            print('  price:', offers.get('price'), offers.get('priceCurrency'))
            print('  desc:', str(found.get('description'))[:100])
        else:
            print('  no JSON-LD product; og:', (og.group(1)[:100] if og else 'none'))
            print('  title:', re.search(r'<title>([^<]+)</title>', h).group(1)[:80])
    except Exception as e:
        print('===', key, 'FAILED:', str(e)[:120])

import re, urllib.request, ssl
ctx = ssl.create_default_context(); ctx.check_hostname = False; ctx.verify_mode = ssl.CERT_NONE
UA = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/126 Safari/537.36'}
html = open('index.html', encoding='utf-8').read()
urls = sorted(set(re.findall(r"url:'(https?://[^']+)'", html)))
print('total unique product/brand urls:', len(urls))
dead = []
for u in urls:
    try:
        req = urllib.request.Request(u, headers=UA, method='GET')
        r = urllib.request.urlopen(req, timeout=25, context=ctx)
        print(r.status, u[:95])
    except urllib.error.HTTPError as e:
        print(e.code, u[:95])
        if e.code in (404, 410): dead.append(u)
    except Exception as e:
        print('ERR', str(e)[:40], u[:95])
print('\nDEAD (404/410):', len(dead))
for u in dead: print('  ', u)

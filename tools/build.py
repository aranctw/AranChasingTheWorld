# -*- coding: utf-8 -*-
"""Genera el sitio completo (ES en raíz, /en/, /it/) en la raíz.   python3 tools/build.py"""
import os, sys, json, glob, hashlib, shutil, html, datetime
sys.path.insert(0, os.path.dirname(__file__))
from content import *
from PIL import Image

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
SITE = ROOT
PHOTOS = os.path.join(ROOT, 'photos')
TODAY = datetime.date.today().isoformat()
E = html.escape
WARN = []

# ------------------------------------------------------------------ iconos (SVG en línea)
ICONS = {
 'wa': '<path d="M7.9 20A9 9 0 1 0 4 16.1L2 22Z"/><path class="f" d="M9.2 8.2c-.3 0-.6.2-.8.5-.5.8-.2 1.9.6 3.1 1 1.6 2.2 2.6 3.6 3.2 1 .4 1.9.3 2.4-.2.2-.3.4-.6.3-.8l-1.6-.9-.8.8c-.9-.4-1.8-1.2-2.2-2.2l.7-.7-.8-1.7c-.1-.3-.4-.5-.8-.1z" fill="currentColor" stroke="none"/>',
 'instagram': '<rect x="2" y="2" width="20" height="20" rx="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><path d="M17.5 6.5h.01"/>',
 'facebook': '<path d="M18 2h-3a5 5 0 0 0-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 0 1 1-1h3z"/>',
 'tiktok': '<path d="M12 3v11.5a3.5 3.5 0 1 1-3.5-3.5"/><path d="M12 3c0 2.6 2 4.6 5 4.6"/>',
 'globe': '<circle cx="12" cy="12" r="10"/><path d="M2 12h20"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/>',
 'arrow': '<path d="M5 12h14"/><path d="m12 5 7 7-7 7"/>',
 'check': '<path d="M20 6 9 17l-5-5"/>',
 'menu': '<path d="M4 7h16"/><path d="M4 12h16"/><path d="M4 17h16"/>',
 'close': '<path d="M18 6 6 18"/><path d="m6 6 12 12"/>',
 'pin': '<path d="M20 10c0 6-8 12-8 12S4 16 4 10a8 8 0 0 1 16 0z"/><circle cx="12" cy="10" r="3"/>',
 'gift': '<rect x="3" y="8" width="18" height="4" rx="1"/><path d="M12 8v13"/><path d="M19 12v7a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2v-7"/><path d="M7.5 8a2.5 2.5 0 0 1 0-5C11 3 12 8 12 8s1-5 4.5-5a2.5 2.5 0 0 1 0 5"/>',
 'plane': '<path d="M17.8 19.2 16 11l3.5-3.5C21 6 21.5 4 21 3c-1-.5-3 0-4.5 1.5L13 8 4.8 6.2c-.5-.1-.9.1-1.1.5l-.3.5c-.2.5-.1 1 .3 1.3L9 12l-2 3H4l-1 1 3 2 2 3 1-1v-3l3-2 3.5 5.3c.3.4.8.5 1.3.3l.5-.2c.4-.3.6-.7.5-1.2z"/>',
 'star': '<path d="m12 2 3.1 6.3 6.9 1-5 4.9 1.2 6.8L12 17.8 5.8 21l1.2-6.8-5-4.9 6.9-1z" fill="currentColor"/>',
}
def icon(name, cls=''):
    return f'<svg class="icon {cls}" viewBox="0 0 24 24" aria-hidden="true" focusable="false">{ICONS[name]}</svg>'

# ------------------------------------------------------------------ ilustraciones propias (sustituyen a las fotos ajenas)
_uid = [0]
def _id(p):
    _uid[0] += 1; return f'{p}{_uid[0]}'

def illo(key):
    g = _id('g')
    W = 'viewBox="0 0 400 250" preserveAspectRatio="xMidYMid slice" aria-hidden="true" focusable="false"'
    if key == 'seda':
        waves = ''.join(f'<path d="M-10 {40+i*14} C 80 {10+i*14}, 140 {90+i*14}, 220 {50+i*14} S 360 {10+i*14}, 420 {60+i*14}" fill="none" stroke="#d4af37" stroke-width="{1+ (i%3)*0.8}" opacity="{0.35+(i%4)*0.15}"/>' for i in range(13))
        return f'<svg {W}><defs><linearGradient id="{g}" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#572364"/><stop offset="1" stop-color="#9b3f87"/></linearGradient></defs><rect width="400" height="250" fill="url(#{g})"/>{waves}<circle cx="318" cy="190" r="34" fill="#f6e9b8" opacity=".95"/><circle cx="318" cy="190" r="22" fill="#d4af37"/><circle cx="318" cy="190" r="8" fill="#572364"/></svg>'
    if key == 'esencial':
        return f'<svg {W}><defs><linearGradient id="{g}" x1="0" y1="0" x2="0" y2="1"><stop stop-color="#2a8a7e"/><stop offset="1" stop-color="#17524b"/></linearGradient></defs><rect width="400" height="250" fill="url(#{g})"/><circle cx="320" cy="62" r="28" fill="#f6e9b8" opacity=".9"/>' \
               '<g fill="#fbf6ec"><rect x="92" y="78" width="62" height="172"/><rect x="246" y="78" width="62" height="172"/><rect x="154" y="120" width="92" height="130"/>' \
               + ''.join(f'<rect x="{x}" y="64" width="12" height="16"/>' for x in (92,112,134,246,266,288)) + \
               '</g><path d="M166 250v-70a34 34 0 0 1 68 0v70z" fill="#17524b"/><rect x="104" y="108" width="14" height="30" rx="7" fill="#17524b"/><rect x="278" y="108" width="14" height="30" rx="7" fill="#17524b"/></svg>'
    if key == 'modernista':
        petals = ''.join(f'<ellipse cx="200" cy="125" rx="16" ry="62" fill="none" stroke="#d4af37" stroke-width="2" transform="rotate({a} 200 125)" opacity=".9"/>' for a in range(0, 180, 22))
        rings = ''.join(f'<circle cx="200" cy="125" r="{r}" fill="none" stroke="#1f6f66" stroke-width="2" opacity=".8"/>' for r in (30, 66, 98))
        return f'<svg {W}><rect width="400" height="250" fill="#2e1237"/>{rings}{petals}<circle cx="200" cy="125" r="10" fill="#d4af37"/><path d="M0 250 Q 100 190 200 250 T 400 250" fill="#572364" opacity=".8"/></svg>'
    if key == 'bici':
        return f'<svg {W}><defs><linearGradient id="{g}" x1="0" y1="0" x2="0" y2="1"><stop stop-color="#7cc3a4"/><stop offset="1" stop-color="#1f6f66"/></linearGradient></defs><rect width="400" height="250" fill="url(#{g})"/><circle cx="68" cy="60" r="26" fill="#fbf6ec" opacity=".85"/>' \
               + ''.join(f'<path d="M-10 {200+i*16} q 40 -14 80 0 t 80 0 t 80 0 t 80 0 t 80 0" fill="none" stroke="#fbf6ec" stroke-width="2.4" opacity="{0.7-i*0.2}"/>' for i in range(3)) + \
               '<g fill="none" stroke="#fbf6ec" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"><circle cx="140" cy="150" r="38"/><circle cx="262" cy="150" r="38"/><path d="M140 150 L186 96 L238 96 L262 150 M186 96 L214 150 L140 150 M214 150 L238 96"/><path d="M178 84h20M232 86l12-8h14"/></g></svg>'
    if key == 'altea':
        houses = ''.join(f'<rect x="{x}" y="{y}" width="{w}" height="{250-y}" fill="#fff" opacity=".96"/><rect x="{x+w*0.3}" y="{y+16}" width="{w*0.22}" height="22" rx="2" fill="#2d6f8f"/>' for x, y, w in ((10,150,62),(76,128,52),(250,140,64),(318,158,72),(150,170,60)))
        return f'<svg {W}><defs><linearGradient id="{g}" x1="0" y1="0" x2="0" y2="1"><stop stop-color="#8fcde0"/><stop offset=".7" stop-color="#2d7ea6"/><stop offset="1" stop-color="#1c5f84"/></linearGradient></defs><rect width="400" height="250" fill="url(#{g})"/><circle cx="336" cy="52" r="26" fill="#f6e9b8"/>{houses}' \
               '<g><rect x="168" y="112" width="64" height="138" fill="#fff"/><path d="M168 112a32 32 0 0 1 64 0z" fill="#2d6f8f"/><path d="M200 62v18M192 70h16" stroke="#fff" stroke-width="3" stroke-linecap="round"/><path d="M186 250v-34a14 14 0 0 1 28 0v34z" fill="#2d6f8f"/></g></svg>'
    if key == 'colombia':
        palms = ''.join(f'<g transform="translate({x} {y}) scale({s})"><path d="M0 0 C 2 -30 -2 -60 3 -90" fill="none" stroke="#5a3a1e" stroke-width="5" stroke-linecap="round"/><g fill="#1f6f66"><path d="M3 -90 q -34 -6 -52 14 q 28 -8 52 -4z"/><path d="M3 -90 q 34 -6 52 14 q -28 -8 -52 -4z"/><path d="M3 -90 q -22 -26 -50 -22 q 30 4 50 22z"/><path d="M3 -90 q 22 -26 50 -22 q -30 4 -50 22z"/><path d="M3 -90 q 0 -30 -4 -40 q 12 14 4 40z"/></g></g>' for x, y, s in ((300, 218, 1), (350, 226, .8), (60, 232, .7)))
        return f'<svg {W}><defs><linearGradient id="{g}" x1="0" y1="0" x2="0" y2="1"><stop stop-color="#f6c94a"/><stop offset=".55" stop-color="#f2a65a"/><stop offset="1" stop-color="#d9658c"/></linearGradient></defs><rect width="400" height="250" fill="url(#{g})"/><circle cx="92" cy="70" r="30" fill="#fbf6ec" opacity=".9"/>' \
               '<path d="M0 170 L70 96 L120 140 L190 70 L262 150 L320 110 L400 170 V250 H0z" fill="#2c8a63"/><path d="M0 190 L60 140 L130 176 L210 120 L290 180 L360 150 L400 176 V250 H0z" fill="#1f6f66"/>' \
               '<path d="M0 214 q 50 -12 100 0 t 100 0 t 100 0 t 100 0 V250 H0z" fill="#3bb5c4"/><path d="M0 232 q 50 -10 100 0 t 100 0 t 100 0 t 100 0 V250 H0z" fill="#2a98ac"/>' + palms + '</svg>'
    if key == 'islandia':
        stars = ''.join(f'<circle cx="{(i*53)%400}" cy="{(i*37)%110+8}" r="{1+(i%3)*0.5}" fill="#fff" opacity="{0.4+(i%4)*0.15}"/>' for i in range(34))
        return f'<svg {W}><defs><linearGradient id="{g}" x1="0" y1="0" x2="0" y2="1"><stop stop-color="#140a1c"/><stop offset="1" stop-color="#3b1a4a"/></linearGradient></defs><rect width="400" height="250" fill="url(#{g})"/>{stars}' \
               '<path d="M-10 120 C 70 40, 130 150, 200 80 S 330 30, 420 100" fill="none" stroke="#5ee0c0" stroke-width="22" opacity=".28"/><path d="M-10 130 C 70 60, 130 160, 200 100 S 330 50, 420 118" fill="none" stroke="#5ee0c0" stroke-width="7" opacity=".6"/>' \
               '<path d="M0 250V170l60-62 44 44 58-80 70 98 52-52 116 82v50z" fill="#27123a"/><path d="M0 250V200l70-48 50 36 80-70 80 78 50-34 70 48v40z" fill="#1f6f66" opacity=".85"/><path d="M162 72l22 32h-44zM234 118l14 20h-28z" fill="#fbf6ec" opacity=".9"/></svg>'
    raise KeyError(key)

def photo_set(key):
    """Si existe photos/<key>.(jpg|png|webp) se usa tu foto en vez de la ilustración."""
    for ext in ('jpg', 'jpeg', 'png', 'webp'):
        p = os.path.join(PHOTOS, f'{key}.{ext}')
        if os.path.exists(p):
            out = os.path.join(SITE, 'assets/img/tours'); os.makedirs(out, exist_ok=True)
            im = Image.open(p).convert('RGB')
            for w in (520, 900):
                h = round(im.height * w / im.width); im.resize((w, h), Image.LANCZOS).save(os.path.join(out, f'{key}-{w}.webp'), 'WEBP', quality=78, method=6)
            return (f'/assets/img/tours/{key}-520.webp', f'/assets/img/tours/{key}-900.webp', round(im.height * 900 / im.width))
    return None

def media(key, alt, lazy=True, eager=False):
    ph = photo_set(key)
    if ph:
        a, b, h = ph
        return f'<img src="{b}" srcset="{a} 520w, {b} 900w" sizes="(min-width:900px) 560px, 100vw" width="900" height="{h}" alt="{E(alt)}" {"" if eager else "loading=\"lazy\" decoding=\"async\""}>'
    return illo(key).replace('aria-hidden="true"', f'role="img" aria-label="{E(alt)}"', 1)

# ------------------------------------------------------------------ URLs
def prefix(lang): return '' if lang == 'es' else f'/{lang}'
def url_home(lang): return '/' if lang == 'es' else f'/{lang}/'
def url_tour(lang, key): t = TOURS[key]; return f"{prefix(lang)}/{t['dir'][lang]}/{t['slug'][lang]}/"
def url_trip(lang, key): return f"{prefix(lang)}/{TRIPS[key]['slug'][lang]}/"
def abs_(u): return DOMAIN + u
def wa(lang, msg): return f'https://wa.me/{PHONE}?text=' + __import__('urllib.parse').parse.quote(msg)
def asset_v(path):
    with open(os.path.join(SITE, path.lstrip('/')), 'rb') as f: return hashlib.md5(f.read()).hexdigest()[:8]

# ------------------------------------------------------------------ trozos comunes
def lang_switch(lang, alts):
    ui = UI[lang]
    links = ''.join(f'<a href="{alts[l]}" hreflang="{l}" lang="{l}" aria-label="{LANG_NAMES[l]}" title="{LANG_NAMES[l]}"{" aria-current=\"true\"" if l == lang else ""}>{l.upper()}</a>' for l in LANGS)
    return f'<nav class="lang" aria-label="{ui["lang_label"]}">{icon("globe")}{links}</nav>'

def header(lang, alts, home_anchor_prefix):
    ui = UI[lang]; hp = home_anchor_prefix
    links = ''.join(f'<a href="{hp}#{a}">{t}</a>' for a, t in ui['nav'])
    wa_url = wa(lang, ui['wa_msg'])
    return f'''<header class="header" id="header"><div class="container nav-wrap">
<a class="brand" href="{url_home(lang)}" aria-label="{BRAND} — {ui['home_label']}"><img src="/assets/img/logo.png" alt="{BRAND}" width="112" height="40"></a>
<nav class="nav" id="site-nav" aria-label="{ui['primary_nav']}">{links}<a class="btn btn-wa nav-cta" href="{wa_url}" target="_blank" rel="noopener">{icon('wa')} {ui['wa_long']}</a></nav>
{lang_switch(lang, alts)}
<a class="btn btn-wa btn-sm header-wa" href="{wa_url}" target="_blank" rel="noopener">{icon('wa')} {ui['wa_btn']}</a>
<button class="nav-toggle" type="button" aria-expanded="false" aria-controls="site-nav" aria-label="{ui['menu']}" data-open="{ui['menu']}" data-close="{ui['close']}">{icon('menu','i-open')}{icon('close','i-close')}</button>
</div></header>'''

def footer(lang):
    ui = UI[lang]
    tours = ''.join(f'<li><a href="{url_tour(lang,k)}">{E(TOURS[k][lang]["name"])}</a></li>' for k in TOUR_ORDER + ['altea'])
    tours += ''.join(f'<li><a href="{url_trip(lang,k)}">{E(TRIPS[k][lang]["name"])}</a></li>' for k in TRIP_ORDER)
    nav = ''.join(f'<li><a href="{url_home(lang)}#{a}">{t}</a></li>' for a, t in ui['nav'])
    legal = ''.join(f'<li><a href="/{a}/">{t}</a>{ui["legal_note"] if lang != "es" else ""}</li>' for a, t in ui['legal'])
    soc = ''.join(f'<a class="social" href="{SOCIAL[n]}" target="_blank" rel="noopener me" aria-label="{n.capitalize()}">{icon(n)}</a>' for n in ('instagram', 'facebook', 'tiktok'))
    return f'''<footer class="footer"><div class="container">
<div class="footer-grid">
<div class="footer-brand"><img src="/assets/img/logo-white.png" alt="{BRAND}" width="157" height="56" loading="lazy"><p>{ui['footer_tag']}</p><div class="socials">{soc}</div></div>
<div><h2>{ui['footer_tours']}</h2><ul>{tours}</ul></div>
<div><h2>{BRAND}</h2><ul>{nav}</ul></div>
<div><h2>{ui['footer_legal']}</h2><ul>{legal}</ul></div>
</div>
<div class="footer-legal"><p><strong>Archer Travel Service, Inc.</strong> — {ui['agent']}</p>
<p><a href="{EVO}" target="_blank" rel="noopener sponsored">{ui['evo']}</a> · <a href="{EXOTICCA}" target="_blank" rel="noopener sponsored">{ui['exo']}</a></p>
<p>{ui['affiliate']}</p><p>© 2026 {BRAND}. {ui['rights']}.</p></div>
</div></footer>
<a class="fab" href="{wa(lang, ui['wa_msg'])}" target="_blank" rel="noopener" aria-label="{ui['wa_long']}">{icon('wa')}</a>'''

def contact_form(lang):
    f = UI[lang]['form']
    opts = ''.join(f'<option value="{v}">{E(t)}</option>' for v, t in f['opts'])
    return f'''<form class="form" action="{FORMSPREE}" method="POST" data-ajax data-sending="{f['sending']}" data-ok="{E(f['ok'])}" data-err="{E(f['err'])}">
<label>{f['name']}<input type="text" name="nombre" autocomplete="name" required></label>
<label>{f['email']}<input type="email" name="email" autocomplete="email" required></label>
<label>{f['interest']}<select name="interes" required><option value="" disabled selected></option>{opts}</select></label>
<label>{f['message'].rstrip('…')}<textarea name="mensaje" rows="5" required></textarea></label>
<input type="hidden" name="idioma" value="{lang}"><input type="hidden" name="_subject" value="Consulta web aranchasingworld.com ({lang})">
<div class="hp" aria-hidden="true"><label>No rellenar<input type="text" name="_gotcha" tabindex="-1" autocomplete="off"></label></div>
<label class="check"><input type="checkbox" name="consentimiento" value="si" required><span>{f['consent']}</span></label>
<button class="btn btn-gold btn-block" type="submit">{f['send']}</button>
<div class="form-status" role="status" aria-live="polite"></div></form>'''

def waitlist_form(lang, key):
    f = UI[lang]['form']; tr = TRIPS[key]; t = tr[lang]
    return f'''<form class="waitlist" action="{FORMSPREE}" method="POST" data-ajax data-sending="{f['sending']}" data-ok="{E(t['ok'])}" data-err="{E(f['err'])}">
<div class="row"><input type="email" name="email" placeholder="{E(f['wl_email'])}" aria-label="{E(f['wl_email'])}" autocomplete="email" required><button class="btn btn-gold" type="submit">{E(t['btn'])}</button></div>
<input type="hidden" name="interes" value="{tr['interes']}"><input type="hidden" name="idioma" value="{lang}"><input type="hidden" name="_subject" value="{tr['subject']} ({lang})">
<div class="hp" aria-hidden="true"><label>No rellenar<input type="text" name="_gotcha" tabindex="-1" autocomplete="off"></label></div>
<label class="check"><input type="checkbox" name="consentimiento" value="si" required><span>{f['wl_consent']}</span></label>
<div class="form-status" role="status" aria-live="polite"></div></form>'''

def head(lang, title, desc, path_alts, canonical, jsonld, noindex=False, og_type='website'):
    css_v, js_v = asset_v('/assets/css/styles.css'), asset_v('/assets/js/main.js')
    alt_tags = ''
    if path_alts:
        alt_tags = ''.join(f'<link rel="alternate" hreflang="{l}" href="{abs_(path_alts[l])}">' for l in LANGS)
        alt_tags += f'<link rel="alternate" hreflang="x-default" href="{abs_(path_alts["es"])}">'
    og_alt = ''.join(f'<meta property="og:locale:alternate" content="{OG_LOCALE[l]}">' for l in LANGS if l != lang) if path_alts else ''
    robots = 'noindex,follow' if noindex else 'index,follow,max-image-preview:large'
    ld = ''.join(f'<script type="application/ld+json">{json.dumps(j, ensure_ascii=False, separators=(",", ":"))}</script>' for j in jsonld)
    img = abs_('/assets/img/og-image.jpg')
    return f'''<!DOCTYPE html>
<html lang="{lang}"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{E(title)}</title><meta name="description" content="{E(desc)}">
<meta name="robots" content="{robots}"><link rel="canonical" href="{abs_(canonical)}">{alt_tags}
<meta name="theme-color" content="#fbf6ec">
<meta property="og:site_name" content="{BRAND}"><meta property="og:type" content="{og_type}"><meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}">
<meta property="og:url" content="{abs_(canonical)}"><meta property="og:image" content="{img}"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:alt" content="{BRAND}">
<meta property="og:locale" content="{OG_LOCALE[lang]}">{og_alt}
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{E(title)}"><meta name="twitter:description" content="{E(desc)}"><meta name="twitter:image" content="{img}">
<link rel="icon" href="/favicon.ico" sizes="48x48"><link rel="icon" type="image/png" sizes="32x32" href="/assets/img/favicon-32.png"><link rel="apple-touch-icon" href="/assets/img/apple-touch-icon.png">
<link rel="preload" href="/assets/fonts/poppins-400.woff" as="font" type="font/woff" crossorigin"><link rel="preload" href="/assets/fonts/poppins-700.woff" as="font" type="font/woff" crossorigin>
<link rel="stylesheet" href="/assets/css/styles.css?v={css_v}">
<script>document.documentElement.classList.add("js")</script>{ld}
</head>
<body><a class="skip" href="#main">{UI[lang]['skip']}</a>
'''.replace('crossorigin">', 'crossorigin>')

def page_end():
    return f'<script src="/assets/js/main.js?v={asset_v("/assets/js/main.js")}" defer></script></body></html>'

def write(path, content):
    full = os.path.join(SITE, path.strip('/'), 'index.html') if path.endswith('/') else os.path.join(SITE, path.strip('/'))
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, 'w', encoding='utf-8') as f: f.write(content)

ORG = {'@type': 'Organization', '@id': DOMAIN + '/#org', 'name': BRAND, 'url': DOMAIN + '/', 'logo': DOMAIN + '/assets/img/icon-512.png',
       'image': DOMAIN + '/assets/img/og-image.jpg', 'sameAs': list(SOCIAL.values()), 'knowsLanguage': ['es', 'it', 'en'],
       'areaServed': [{'@type': 'City', 'name': 'Valencia'}, {'@type': 'City', 'name': 'Altea'}]}

def tour_card(lang, key):
    t = TOURS[key][lang]; ui = UI[lang]
    return f'''<article class="card reveal"><div class="card-media">{media(key, t['alt'])}</div><div class="card-body">
<span class="tag">{E(t['tag'])}</span><h4><a href="{url_tour(lang,key)}">{E(t['name'])}</a></h4><p>{E(t['short'])}</p>
<span class="link-arrow">{ui['more_info']} {icon('arrow')}</span></div></article>'''

# ------------------------------------------------------------------ HOME
CAR = {'es': ('Anterior', 'Siguiente', 'Ir a', 'carrusel'), 'en': ('Previous', 'Next', 'Go to', 'carousel'), 'it': ('Precedente', 'Successivo', 'Vai a', 'carosello')}

def alts_home(): return {l: url_home(l) for l in LANGS}

def build_home(lang):
    ui, h = UI[lang], HOME[lang]; alts = alts_home()
    trust = ''.join(f'<li>{icon(i)}<div><strong>{a}</strong><span>{b}</span></div></li>' for i, a, b in h['trust'])
    cards = ''.join(tour_card(lang, k) for k in TOUR_ORDER)
    al = TOURS['altea'][lang]
    reviews = ''.join(f'<figure class="review reveal"><div class="stars" role="img" aria-label="5/5">{icon("star")*5}</div><blockquote><p>“{E(q)}”</p></blockquote><figcaption><strong>{E(n)}</strong><span>{E(c)}</span></figcaption></figure>' for q, n, c in h['reviews'])
    faq = ''.join(f'<details><summary>{E(q)}</summary><p>{E(a)}</p></details>' for q, a in h['faq'])
    chips = ''.join(f'<li>{E(c)}</li>' for c in h['about_chips'])
    about_p = ''.join(f'<p>{E(p)}</p>' for p in h['about_p'])
    cl = CAR[lang]
    slides = ''; dots = ''
    for n, k in enumerate(TRIP_ORDER, 1):
        t = TRIPS[k][lang]
        pts = ''.join(f'<li>{icon("check")}{E(p)}</li>' for p in t['pts'])
        slides += f'''<article class="trip-slide" id="viaje-{k}" role="group" aria-roledescription="{cl[3]}" aria-label="{n} / {len(TRIP_ORDER)}"><div class="trip-grid"><div class="media">{media(k, t['alt'])}</div>
<div><span class="tag">{E(t['badge'])}</span><span class="kicker" style="display:flex">{h['trip_k']}</span><h2>{E(t['name'])}</h2><p>{E(t['card_p'])}</p><ul class="pts">{pts}</ul><p style="font-weight:500;color:#fff">{E(t['wl'])}</p>{waitlist_form(lang, k)}<p style="margin-top:18px"><a class="link-arrow" style="color:#fff" href="{url_trip(lang,k)}">{h['trip_more']} {icon('arrow')}</a></p></div></div></article>'''
        dots += f'<button type="button" class="car-dot" aria-label="{E(cl[2])} {E(t["name"])}"></button>'
    trip_section = f'''<section class="section trip" id="viajes"><div class="container"><div class="carousel reveal" role="group" aria-roledescription="{cl[3]}" aria-label="{E(h['trip_k'])}">
<div class="carousel-track" tabindex="0">{slides}</div>
<div class="carousel-ctrl"><button type="button" class="car-btn" data-dir="-1" aria-label="{cl[0]}">{icon('arrow')}</button><div class="car-dots">{dots}</div><button type="button" class="car-btn" data-dir="1" aria-label="{cl[1]}">{icon('arrow')}</button></div></div></div></section>'''
    jsonld = [
        {'@context': 'https://schema.org', '@graph': [ORG, {'@type': 'WebSite', '@id': DOMAIN + '/#site', 'url': DOMAIN + '/', 'name': BRAND, 'publisher': {'@id': DOMAIN + '/#org'}, 'inLanguage': ['es', 'en', 'it']}]},
        {'@context': 'https://schema.org', '@type': 'FAQPage', 'inLanguage': lang, 'mainEntity': [{'@type': 'Question', 'name': q, 'acceptedAnswer': {'@type': 'Answer', 'text': a}} for q, a in h['faq']]},
    ]
    out = head(lang, h['title'], h['desc'], alts, url_home(lang), jsonld)
    out += header(lang, alts, '') + f'''<main id="main">
<section class="hero"><svg class="hero-flight" viewBox="0 0 1200 600" preserveAspectRatio="none" aria-hidden="true"><path d="M-20 540C300 590 420 130 760 230S1100 70 1230 100" fill="none" stroke="currentColor" stroke-width="2.5" stroke-dasharray="2 12" stroke-linecap="round" vector-effect="non-scaling-stroke"/></svg>
<div class="container hero-grid"><div class="hero-copy"><span class="eyebrow">{icon('pin')} {E(h['eyebrow'])}</span><h1>{h['h1']}</h1><p class="lead">{E(h['lead'])}</p>
<div class="hero-actions"><a class="btn btn-gold" href="#tours">{h['cta1']}</a><a class="btn btn-wa" href="{wa(lang, ui['wa_msg'])}" target="_blank" rel="noopener">{icon('wa')} {h['cta2']}</a></div></div>
<div class="hero-media"><div class="arch"><img src="/assets/img/hero-960.webp" srcset="/assets/img/hero-600.webp 600w, /assets/img/hero-960.webp 960w" sizes="(min-width:900px) 440px, 78vw" width="960" height="1200" alt="{E(h['photo_alt'])}" fetchpriority="high"></div>
<div class="stamp" aria-hidden="true"><svg viewBox="0 0 120 120"><defs><path id="circ" d="M60 60m-46 0a46 46 0 1 1 92 0a46 46 0 1 1-92 0"/></defs><text><textPath href="#circ" textLength="284" lengthAdjust="spacing">{E(h['stamp'])}</textPath></text></svg>{icon('plane')}</div></div></div></section>
<section class="trust" aria-label="{BRAND}"><div class="container"><ul>{trust}</ul></div></section>
<section class="section intro"><div class="container intro-grid reveal"><div><span class="kicker">{h['intro_k']}</span><h2 class="h2">{h['intro_h']}</h2></div><div><p>{E(h['intro_p1'])}</p><p>{h['intro_p2']}</p></div></div></section>
<section class="section" id="tours" style="padding-top:0"><div class="container">
<div class="section-head reveal"><span class="kicker">{h['tours_k']}</span><h2>{h['tours_h']}</h2><p>{E(h['tours_p'])}</p></div>
<div class="dest-head"><span class="dest-num">01</span><h3>{h['val_h']}</h3><p>{E(h['val_p'])}</p></div>
<div class="cards four">{cards}</div>
<div class="note reveal">{icon('gift')}<div><strong>{ui['free_note_t']}</strong><p>{ui['free_note']}</p></div></div>
<div class="dest-head"><span class="dest-num">02</span><h3>{h['alt_h']}</h3><p>{E(h['alt_p'])}</p></div>
<article class="feature reveal"><div class="media">{media('altea', al['alt'])}</div><div class="feature-body"><span class="tag">{E(al['tag'])}</span><h4><a href="{url_tour(lang,'altea')}" style="color:inherit;text-decoration:none">{E(al['name'])}</a></h4><p>{E(al['lead'][0])}</p><p>{E(al['lead'][1])}</p><a class="btn btn-purple" href="{url_tour(lang,'altea')}">{ui['ask_tour']}</a></div></article>
<div class="private reveal"><div><span class="kicker">{h['priv_k']}</span><h3>{h['priv_h']}</h3><p>{E(h['priv_p'])}</p></div><a class="btn btn-gold" href="{wa(lang, ui['wa_private'])}" target="_blank" rel="noopener">{h['priv_btn']}</a></div>
</div></section>
{trip_section}
<section class="section about" id="sobre-mi"><div class="container about-grid"><div class="about-photo reveal"><img src="/assets/img/about-1400.webp" srcset="/assets/img/about-800.webp 800w, /assets/img/about-1400.webp 1400w" sizes="(min-width:900px) 520px, 100vw" width="1400" height="1050" alt="{E(h['about_photo_alt'])}" loading="lazy" decoding="async"></div>
<div class="about-copy reveal"><span class="kicker">{h['about_k']}</span><h2 class="h2" style="margin-bottom:20px">{h['about_h']}</h2>{about_p}<ul class="chips">{chips}</ul></div></div></section>
<section class="section reviews" id="opiniones"><div class="container"><div class="section-head reveal"><span class="kicker">{h['rev_k']}</span><h2>{h['rev_h']}</h2></div><div class="review-grid">{reviews}</div></div></section>
<section class="section" id="faq"><div class="container"><div class="section-head reveal"><h2>{h['faq_h']}</h2></div><div class="faq-list reveal">{faq}</div></div></section>
<section class="section contact" id="contacto"><div class="container contact-grid"><div class="contact-info reveal"><span class="kicker">{h['ct_k']}</span><h2>{h['ct_h']}</h2><p>{E(h['ct_p'])}</p>
<div class="contact-wa"><a class="btn btn-wa" href="{wa(lang, ui['wa_msg'])}" target="_blank" rel="noopener">{icon('wa')} {ui['wa_long']}</a></div>
<span class="socials-label">{ui['follow']}</span><div class="socials">{''.join(f'<a class="social" href="{SOCIAL[n]}" target="_blank" rel="noopener me" aria-label="{n.capitalize()}">{icon(n)}</a>' for n in ('instagram','facebook','tiktok'))}</div></div>
<div class="reveal">{contact_form(lang)}</div></div></section>
</main>''' + footer(lang) + page_end()
    write(url_home(lang), out)

# ------------------------------------------------------------------ TOUR / VIAJE
def alts_tour(key): return {l: url_tour(l, key) for l in LANGS}
def alts_trip(key): return {l: url_trip(l, key) for l in LANGS}

def crumbs(lang, label, current_url):
    ui = UI[lang]
    return f'<nav class="crumbs container" aria-label="{ui["breadcrumb"]}"><ol><li><a href="{url_home(lang)}">{ui["home_label"]}</a></li><li><a href="{url_home(lang)}#tours">{HOME[lang]["tours_h"]}</a></li><li aria-current="page">{E(label)}</li></ol></nav>'

def breadcrumb_ld(lang, label, current_url):
    ui = UI[lang]
    return {'@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': [
        {'@type': 'ListItem', 'position': 1, 'name': ui['home_label'], 'item': abs_(url_home(lang))},
        {'@type': 'ListItem', 'position': 2, 'name': HOME[lang]['tours_h'], 'item': abs_(url_home(lang) + '#tours')},
        {'@type': 'ListItem', 'position': 3, 'name': label, 'item': abs_(current_url)}]}

def build_tour(lang, key):
    ui, t = UI[lang], TOURS[key][lang]; alts = alts_tour(key); cur = url_tour(lang, key)
    pr = PRACTICAL[key]; kind = TOUR_KIND[key]
    hl = ''.join(f'<li>{icon("check")}<span>{E(x)}</span></li>' for x in t['hl'])
    lead = ''.join(f'<p>{E(p)}</p>' for p in t['lead'])
    msg = ui['wa_tour'].format(n=t['name']); wl = wa(lang, msg)
    others = [k for k in TOUR_ORDER + ['altea'] if k != key]
    i = (TOUR_ORDER + ['altea']).index(key); order = (TOUR_ORDER + ['altea'])
    rel = [order[(i + n) % len(order)] for n in (1, 2, 3)]
    side = f'''<aside class="side reveal"><div class="side-card"><h2>{ui['practical']}</h2><dl>
<div><dt>{ui['type']}</dt><dd>{ui['type_free'] if kind == 'free' else ui['type_guided']}</dd></div>
<div><dt>{ui['languages']}</dt><dd>{ui['languages_v']}</dd></div>
<div><dt>{ui['duration']}</dt><dd>{E(pr['duration']) if pr['duration'] else ui['duration_tbc']}</dd></div>
<div><dt>{ui['meeting']}</dt><dd>{E(pr['meeting']) if pr['meeting'] else ui['meeting_tbc']}</dd></div>
<div><dt>{ui['booking']}</dt><dd>{ui['booking_v']}</dd></div></dl>
<a class="btn btn-wa btn-block" href="{wl}" target="_blank" rel="noopener">{icon('wa')} {ui['book_wa']}</a>
<a class="btn btn-ghost btn-block" href="{url_home(lang)}#contacto">{ui['form']['send']}</a></div></aside>'''
    free_note = f'<section><div class="note">{icon("gift")}<div><strong>{ui["free_note_t"]}</strong><p>{ui["free_note"]}</p></div></div></section>' if kind == 'free' else ''
    jsonld = [{'@context': 'https://schema.org', '@type': 'TouristTrip', 'name': t['name'], 'description': t['desc'], 'url': abs_(cur), 'inLanguage': lang, 'provider': {'@id': DOMAIN + '/#org'}, 'touristType': 'Cultural tourism'},
              breadcrumb_ld(lang, t['name'], cur)]
    out = head(lang, t['title'], t['desc'], alts, cur, jsonld) + header(lang, alts, url_home(lang)) + f'''<main id="main">{crumbs(lang, t['name'], cur)}
<section class="page-hero"><div class="container page-hero-grid"><div><span class="tag{" gold" if kind != "free" else ""}">{E(t['tag'])}</span><h1>{E(t['h1'])}</h1><div class="lead">{lead}</div>
<div class="hero-actions"><a class="btn btn-wa" href="{wl}" target="_blank" rel="noopener">{icon('wa')} {ui['book_wa']}</a><a class="btn btn-ghost" href="{url_home(lang)}#tours">{ui['back_all']}</a></div></div>
<div class="media">{media(key, t['alt'], eager=True)}</div></div></section>
<div class="container tour-layout"><div class="tour-main"><section class="reveal"><h2>{ui['seeing']}</h2><ul class="ticks">{hl}</ul></section>{free_note}
<section class="reveal"><h2>{ui['faq']}</h2><div class="faq-list">{''.join(f'<details><summary>{E(q)}</summary><p>{E(a)}</p></details>' for q, a in (HOME[lang]['faq'][:4] if kind == 'free' else HOME[lang]['faq'][1:5]))}</div></section></div>{side}</div>
<section class="related"><div class="container"><h2>{ui['more_tours']}</h2><div class="cards" style="grid-template-columns:repeat(auto-fit,minmax(250px,1fr))">{''.join(tour_card(lang, k) for k in rel)}</div></div></section>
</main>''' + footer(lang) + page_end()
    write(cur, out)

def build_trip(lang, key):
    ui, t = UI[lang], TRIPS[key][lang]; alts = alts_trip(key); cur = url_trip(lang, key); h = HOME[lang]
    hl = ''.join(f'<li>{icon("check")}<span>{E(x)}</span></li>' for x in t['hl'])
    lead = ''.join(f'<p>{E(p)}</p>' for p in t['lead'])
    wl = wa(lang, t['wa'])
    side = f'''<aside class="side reveal"><div class="side-card" style="background:var(--purple-deep);color:#fff"><h2 style="color:#fff">{E(t['badge'])} · {E(t['name'])}</h2>
<dl><div><dt style="color:var(--gold)">{ui['type']}</dt><dd style="color:#fff">{E(t['type'])}</dd></div><div><dt style="color:var(--gold)">{ui['duration']}</dt><dd style="color:#fff">{E(t['hl'][2])}</dd></div></dl>
<p style="font-weight:500">{E(t['wl'])}</p>{waitlist_form(lang, key)}<a class="btn btn-wa btn-block" style="margin-top:14px" href="{wl}" target="_blank" rel="noopener">{icon('wa')} {ui['wa_long']}</a></div></aside>'''
    crumb = f'<nav class="crumbs container" aria-label="{ui["breadcrumb"]}"><ol><li><a href="{url_home(lang)}">{ui["home_label"]}</a></li><li><a href="{url_home(lang)}#viajes">{h["trip_k"]}</a></li><li aria-current="page">{E(t["name"])}</li></ol></nav>'
    jsonld = [{'@context': 'https://schema.org', '@type': 'TouristTrip', 'name': t['name'], 'description': t['desc'], 'url': abs_(cur), 'inLanguage': lang, 'provider': {'@id': DOMAIN + '/#org'}},
              {'@context': 'https://schema.org', '@type': 'BreadcrumbList', 'itemListElement': [
                  {'@type': 'ListItem', 'position': 1, 'name': ui['home_label'], 'item': abs_(url_home(lang))},
                  {'@type': 'ListItem', 'position': 2, 'name': t['name'], 'item': abs_(cur)}]}]
    out = head(lang, t['title'], t['desc'], alts, cur, jsonld) + header(lang, alts, url_home(lang)) + f'''<main id="main">{crumb}
<section class="page-hero"><div class="container page-hero-grid"><div><span class="tag gold">{E(t['tag'])}</span><h1>{E(t['h1'])}</h1><div class="lead">{lead}</div></div><div class="media">{media(key, t['alt'], eager=True)}</div></div></section>
<div class="container tour-layout"><div class="tour-main"><section class="reveal"><h2>{h['trip_k']}</h2><ul class="ticks">{hl}</ul></section>
<section class="reveal"><h2>{ui['faq']}</h2><div class="faq-list">{''.join(f'<details><summary>{E(q)}</summary><p>{E(a)}</p></details>' for q, a in h['faq'][1:])}</div></section></div>{side}</div>
<section class="related"><div class="container"><h2>{ui['more_tours']}</h2><div class="cards" style="grid-template-columns:repeat(auto-fit,minmax(250px,1fr))">{''.join(tour_card(lang, k) for k in TOUR_ORDER[:3])}</div></div></section>
</main>''' + footer(lang) + page_end()
    write(cur, out)

# ------------------------------------------------------------------ LEGAL (ES) y 404
def own(k, label):
    v = OWNER.get(k)
    if v: return E(v)
    WARN.append(f'OWNER["{k}"] vacío (aparece resaltado en las páginas legales)')
    return f'<mark class="todo">COMPLETAR: {label}</mark>'

def legal_page(slug, title, body, desc):
    lang = 'es'; alts = None
    out = head(lang, f'{title} | {BRAND}', desc, None, f'/{slug}/', [], noindex=False)
    out += header(lang, {l: url_home(l) for l in LANGS}, '/') + f'<main id="main"><div class="container"><div class="prose reveal"><h1>{title}</h1>{body}<p><small>Última actualización: {TODAY}</small></p></div></div></main>' + footer(lang) + page_end()
    write(f'/{slug}/', out)

def build_legal():
    owner = f'''<ul><li><strong>Titular:</strong> {own('nombre', 'nombre y apellidos')}</li><li><strong>NIF/NIE:</strong> {own('nif', 'NIF')}</li><li><strong>Domicilio:</strong> {own('domicilio', 'domicilio')}</li><li><strong>Correo electrónico:</strong> {own('email', 'email de contacto')}</li><li><strong>Sitio web:</strong> {DOMAIN}</li></ul>'''
    legal_page('aviso-legal', 'Aviso legal', f'''<h2>1. Datos identificativos</h2><p>En cumplimiento del artículo 10 de la Ley 34/2002, de servicios de la sociedad de la información y de comercio electrónico (LSSI-CE), se informa de que este sitio web es titularidad de:</p>{owner}
<h2>2. Objeto</h2><p>Este sitio presenta los tours, free tours y experiencias de {BRAND} en Valencia y Altea, así como información sobre viajes privados.</p>
<h2>3. Propiedad intelectual</h2><p>Los textos, el diseño, el logotipo y las imágenes propias de este sitio pertenecen a su titular. Queda prohibida su reproducción sin autorización.</p>
<h2>4. Servicios de terceros y enlaces</h2><p>Esta web incluye enlaces a Evo Travel y Exoticca, a través de Archer Travel Service, Inc. Las reservas de esos viajes se contratan y gestionan con dichas empresas, que son responsables de sus condiciones. Los enlaces externos se ofrecen a título informativo y el titular no responde de sus contenidos.</p>
<h2>5. Legislación aplicable</h2><p>Este aviso se rige por la legislación española. Para cualquier controversia serán competentes los juzgados y tribunales que correspondan conforme a la normativa vigente.</p>''', 'Aviso legal e información del titular del sitio web aranchasingworld.com.')
    legal_page('privacidad', 'Política de privacidad', f'''<h2>1. Responsable del tratamiento</h2>{owner}
<h2>2. Qué datos tratamos y para qué</h2><ul><li><strong>Formulario de contacto:</strong> nombre, correo electrónico, interés, idioma y mensaje, para responder a tu consulta o gestionar tu reserva.</li><li><strong>Información y lista de espera de los viajes (Colombia e Islandia):</strong> correo electrónico e idioma, para enviarte la información del viaje o avisarte cuando se abran plazas.</li></ul>
<h2>3. Base jurídica</h2><p>Tu consentimiento (art. 6.1.a RGPD) al marcar la casilla y enviar el formulario, y la aplicación de medidas precontractuales a petición tuya cuando solicitas información o reserva (art. 6.1.b RGPD).</p>
<h2>4. Destinatarios y transferencias</h2><p>Los formularios se gestionan mediante Formspree (Formspree, Inc.), proveedor con servidores en Estados Unidos que actúa como encargado del tratamiento, con las garantías previstas en el RGPD para las transferencias internacionales. No se ceden datos a otros terceros salvo obligación legal. Si me escribes por WhatsApp, WhatsApp trata también tus datos según su propia política.</p>
<h2>5. Conservación</h2><p>Conservaré tus datos el tiempo necesario para atender tu consulta o, en las solicitudes de información y listas de espera de los viajes, hasta que te des de baja o el viaje se haya comunicado o realizado, y después durante los plazos legales aplicables.</p>
<h2>6. Tus derechos</h2><p>Puedes ejercer tus derechos de acceso, rectificación, supresión, oposición, limitación y portabilidad escribiendo a {own('email', 'email de contacto')}. Si consideras que no se han atendido, puedes reclamar ante la Agencia Española de Protección de Datos (www.aepd.es).</p>''', 'Política de privacidad de aranchasingworld.com: qué datos se tratan, para qué y cómo ejercer tus derechos.')
    legal_page('cookies', 'Política de cookies', '''<h2>Uso de cookies</h2><p>Este sitio web <strong>no utiliza cookies propias ni de terceros</strong> para analítica, publicidad o personalización. Las fuentes tipográficas y los iconos se sirven desde este mismo dominio, por lo que no se envían datos de tu navegación a terceros al cargar la página.</p>
<h2>Servicios externos</h2><p>Al enviar un formulario, tus datos se transmiten a Formspree para entregármelos (consulta la <a href="/privacidad/">política de privacidad</a>). Los enlaces a Instagram, Facebook, TikTok, WhatsApp, Evo Travel o Exoticca te llevan a sitios externos con sus propias políticas.</p>
<h2>Cambios</h2><p>Si en el futuro se añaden herramientas de analítica u otros servicios que utilicen cookies, se actualizará esta política y se solicitará tu consentimiento antes de activarlas.</p>''', 'Política de cookies de aranchasingworld.com.')

def build_404():
    out = head('es', f'Página no encontrada | {BRAND}', 'La página que buscas no existe.', None, '/404.html', [], noindex=True)
    out += header('es', {l: url_home(l) for l in LANGS}, '/') + f'''<main id="main"><div class="container notfound"><h1>404</h1><p style="font-size:1.2rem;color:var(--muted)">No encuentro esta página… pero el mundo sigue ahí fuera.</p>
<p><a class="btn btn-gold" href="/">Ir al inicio</a> <a class="btn btn-ghost" href="/en/">English</a> <a class="btn btn-ghost" href="/it/">Italiano</a></p></div></main>''' + footer('es') + page_end()
    write('/404.html', out)

# ------------------------------------------------------------------ sitemap / robots / etc.
def build_misc():
    groups = [alts_home()] + [alts_tour(k) for k in TOURS] + [alts_trip(k) for k in TRIP_ORDER]
    urls = ''
    for g in groups:
        for l in LANGS:
            links = ''.join(f'<xhtml:link rel="alternate" hreflang="{x}" href="{abs_(g[x])}"/>' for x in LANGS) + f'<xhtml:link rel="alternate" hreflang="x-default" href="{abs_(g["es"])}"/>'
            urls += f'<url><loc>{abs_(g[l])}</loc><lastmod>{TODAY}</lastmod>{links}</url>\n'
    with open(os.path.join(SITE, 'sitemap.xml'), 'w', encoding='utf-8') as f:
        f.write(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n{urls}</urlset>\n')
    open(os.path.join(SITE, 'robots.txt'), 'w').write(f'User-agent: *\nAllow: /\n\nSitemap: {DOMAIN}/sitemap.xml\n')
    open(os.path.join(SITE, 'CNAME'), 'w').write('aranchasingworld.com')
    open(os.path.join(SITE, '.nojekyll'), 'w').write('')
    Image.open(os.path.join(SITE, 'assets/img/favicon-48.png')).save(os.path.join(SITE, 'favicon.ico'), sizes=[(48, 48), (32, 32)])
    # URL antigua: redirige a la versión inglesa nueva
    open(os.path.join(SITE, 'index-en.html'), 'w').write(f'<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><title>{BRAND}</title><link rel="canonical" href="{DOMAIN}/en/"><meta http-equiv="refresh" content="0; url=/en/"><meta name="robots" content="noindex,follow"></head><body><a href="/en/">{DOMAIN}/en/</a></body></html>')

def main():
    os.makedirs(SITE, exist_ok=True)
    shutil.copy(os.path.join(ROOT, 'tools/styles.css'), os.path.join(SITE, 'assets/css/styles.css'))
    shutil.copy(os.path.join(ROOT, 'tools/main.js'), os.path.join(SITE, 'assets/js/main.js'))
    for l in LANGS:
        build_home(l)
        for k in TRIP_ORDER: build_trip(l, k)
        for k in TOURS: build_tour(l, k)
    build_legal(); build_404(); build_misc()
    n = sum(len(fs) for _, _, fs in os.walk(SITE))
    print(f'OK: {n} archivos en {SITE}')
    for w in sorted(set(WARN)): print('AVISO:', w)

if __name__ == '__main__':
    main()

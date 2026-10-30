"""Genera le pagine per Google (guide, video, sitemap, robots, dati strutturati).
Uso: python3 tools/seo_build.py https://indirizzo-definitivo  (rilanciare quando cambia l'indirizzo)"""
import sys, os, json, html, datetime
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = (sys.argv[1] if len(sys.argv) > 1 else 'https://boomflashnbuy.com').rstrip('/')
TODAY = datetime.date.today().isoformat()
VIDEO = '/media/BoomFlashnBuy-it-orizzontale.mp4'
VIDEO_V = '/media/BoomFlashnBuy-it-verticale.mp4'
POSTER = '/media/video-poster.jpg'
OG = '/media/og-image.png'
LEGAL = 'A te non costa nulla: mi paga Amazon. In qualità di Affiliato Amazon ricevo un guadagno dagli acquisti idonei.'

CSS = '''*{box-sizing:border-box}html{-webkit-text-size-adjust:100%}body{margin:0;background:#0B0C0A;color:#fff;font:500 17px/1.6 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}
a{color:#D4FF4A}.w{max-width:760px;margin:0 auto;padding:20px 16px 40px}
header{display:flex;align-items:center;gap:12px;padding:8px 0 18px}header img{width:44px;height:44px;border-radius:11px}header a{color:#fff;text-decoration:none;font:italic 900 22px system-ui}header em{font-style:inherit;color:#D4FF4A}
h1{font:italic 900 clamp(30px,7vw,46px)/1.08 system-ui;margin:6px 0 14px;letter-spacing:-.5px}h1 em{font-style:inherit;color:#D4FF4A}
h2{font:italic 900 26px/1.2 system-ui;margin:34px 0 10px}.lead{font-size:19px;color:#d6dcd0}
.cta{display:flex;gap:10px;flex-wrap:wrap;margin:22px 0}.btn{display:inline-flex;align-items:center;gap:8px;background:#D4FF4A;color:#0B0C0A;font-weight:800;text-decoration:none;border-radius:99px;padding:14px 22px}.btn.g{background:none;color:#fff;border:2px solid #D4FF4A}
video{width:100%;border-radius:18px;background:#000;display:block;margin:18px 0}
ol,ul{padding-left:22px}li{margin:6px 0}.box{background:#171914;border:1px solid #2B2F27;border-radius:16px;padding:16px 18px;margin:18px 0}
details{background:#171914;border:1px solid #2B2F27;border-radius:14px;padding:12px 16px;margin:10px 0}summary{font-weight:800;cursor:pointer}
nav.more a{display:block;padding:10px 0;border-top:1px solid #2B2F27;text-decoration:none}
footer{color:#8f988a;font-size:13px;margin-top:40px;border-top:1px solid #2B2F27;padding-top:16px}'''

APP_LD = {"@context": "https://schema.org", "@type": "WebApplication", "name": "BoomFlashnBuy",
  "url": BASE + "/", "applicationCategory": "ShoppingApplication", "operatingSystem": "iOS, Android, Web",
  "description": "Scansiona il codice a barre in negozio e confronta il prezzo con Amazon. Oppure scrivi o di' cosa cerchi. Gratis, senza registrazione.",
  "image": BASE + "/icons/icon-512.png", "inLanguage": ["it", "en", "es", "fr", "de", "pt"],
  "offers": {"@type": "Offer", "price": "0", "priceCurrency": "EUR"}}
VIDEO_LD = {"@context": "https://schema.org", "@type": "VideoObject", "name": "BoomFlashnBuy: prezzo negozio vs Amazon in un lampo",
  "description": "In 30 secondi: scansioni il codice a barre in negozio, confronti il prezzo con Amazon, apri lo scanner con “Ehi Siri: boom!” e cerchi anche a voce.",
  "thumbnailUrl": [BASE + POSTER], "uploadDate": TODAY, "duration": "PT1M4S",
  "contentUrl": BASE + VIDEO, "embedUrl": BASE + "/video/", "inLanguage": "it"}

def faq_ld(faq):
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": html.unescape(a.replace('<b>', '').replace('</b>', ''))}} for q, a in faq]}

def page(slug, title, desc, h1, body, faq=None, video=True, extra_ld=()):
    url = BASE + slug
    lds = [APP_LD] + ([VIDEO_LD] if video else []) + ([faq_ld(faq)] if faq else []) + list(extra_ld)
    vid = (f'<video class="bfb" controls playsinline preload="metadata" poster="{POSTER}"><source src="{VIDEO}" type="video/mp4"></video>'
           + "<script>(function(){var L=['it','en','es','fr','de','pt'],q=new URLSearchParams(location.search).get('lang'),"
             "c=[q].concat(navigator.languages||[navigator.language]),g='en';"
             "for(var i=0;i<c.length;i++){var x=String(c[i]||'').slice(0,2).toLowerCase();if(L.indexOf(x)>=0){g=x;break}}"
             "var o=matchMedia('(orientation:portrait)').matches?'verticale':'orizzontale';"
             "document.querySelectorAll('video.bfb').forEach(function(v){var u='/media/BoomFlashnBuy-'+g+'-'+o+'.mp4';"
             "if(v.currentSrc.indexOf(u)<0){v.querySelector('source').src=u;v.load()}})})()</script>") if video else ''
    fq = ''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q, a in (faq or []))
    more = ''.join(f'<a href="{s}">{t} →</a>' for s, t, *_ in PAGES if s != slug)
    return f'''<!doctype html><html lang="it"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)}</title><meta name="description" content="{html.escape(desc)}"><link rel="canonical" href="{url}">
<meta property="og:type" content="website"><meta property="og:title" content="{html.escape(title)}"><meta property="og:description" content="{html.escape(desc)}"><meta property="og:url" content="{url}"><meta property="og:image" content="{BASE}{OG}"><meta property="og:locale" content="it_IT">
<meta property="og:video" content="{BASE}{VIDEO}"><meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/icons/favicon-48.png"><link rel="apple-touch-icon" href="/icons/apple-touch-icon.png"><meta name="theme-color" content="#0B0C0A">
<style>{CSS}</style>{''.join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in lds)}</head>
<body><div class="w"><header><img src="/icons/icon-192.png" alt="" width="44" height="44"><a href="/">Boom<em>Flash</em>nBuy</a></header>
<main><h1>{h1}</h1>{body.replace('[[VIDEO]]', vid)}
<div class="cta"><a class="btn" href="/?boom=1">📷 Apri lo scanner</a><a class="btn g" href="/">Apri l’app</a></div>
{('<h2>Domande frequenti</h2>' + fq) if fq else ''}
<h2>Altre guide</h2><nav class="more">{more}</nav></main>
<footer>BoomFlashnBuy è gratis e funziona dal browser, senza registrazione. {LEGAL}<br>Aggiornato il {TODAY}.</footer></div></body></html>'''

CTA_STEPS = '''<ol><li>Apri <a href="/">BoomFlashnBuy</a> dal telefono (o di' <b>“Ehi Siri: boom!”</b> su iPhone).</li>
<li>Inquadra il <b>codice a barre</b> del prodotto: al bip l'app lo riconosce.</li>
<li>Se vuoi, scrivi il <b>prezzo che vedi in negozio</b>.</li>
<li>Tocca <b>“Trovato! Vai ai prezzi”</b>: si apre Amazon con tutte le offerte per quel prodotto.</li></ol>'''

PAGES = [
 ('/guide/negozio-o-amazon/', 'Conviene comprare in negozio o su Amazon? Come scoprirlo in 5 secondi',
  'Sei in negozio e non sai se su Amazon costa meno? Scansiona il codice a barre e confronta il prezzo in pochi secondi, gratis.',
  'Negozio o Amazon: <em>dove conviene?</em>',
  '''<p class="lead">Sei davanti allo scaffale, il prezzo sembra buono, ma ti viene il dubbio: e se online costasse meno? Controllarlo a mano vuol dire scrivere il nome giusto, il formato giusto, scorrere i risultati. Con il codice a barre basta un attimo.</p>
[[VIDEO]]<h2>Come confrontare il prezzo in 4 passi</h2>''' + CTA_STEPS + '''
<div class="box"><b>Il trucco:</b> il codice a barre (EAN) identifica il prodotto esatto, compreso il formato. Così confronti la stessa cosa, non un prodotto simile.</div>
<h2>Quando conviene il negozio</h2><ul><li>Ti serve <b>subito</b> e non vuoi aspettare la consegna.</li><li>Il negozio ha un'<b>offerta</b> o un prezzo uguale a quello online.</li><li>Vuoi vedere, provare o farti consigliare.</li></ul>
<h2>Quando conviene Amazon</h2><ul><li>Il prezzo è <b>più basso</b> e puoi aspettare la consegna.</li><li>Trovi <b>formati</b> o confezioni multiple più convenienti.</li><li>Vuoi confrontare più venditori e leggere le recensioni.</li></ul>
<p>BoomFlashnBuy ti tiene anche il conto: se scrivi il prezzo del negozio e poi quello che hai pagato su Amazon, vedi quanto hai risparmiato in totale.</p>''',
  [('Serve installare qualcosa?', 'No. BoomFlashnBuy funziona dal browser del telefono. Se vuoi, puoi aggiungerla alla schermata Home come un’app.'),
   ('È gratis?', 'Sì, è gratis e senza registrazione. L’app riceve una piccola commissione da Amazon sugli acquisti idonei, senza costi per te.'),
   ('E se il prodotto non ha il codice a barre?', 'Puoi usare “Leggi l’etichetta”: l’app legge marca e modello dal testo. Oppure scrivi o di’ cosa cerchi.')]),
 ('/guide/app-scanner-codice-a-barre/', 'App gratis per scansionare il codice a barre e confrontare i prezzi',
  'Scanner per codici a barre gratuito che funziona dal browser: inquadri il codice in negozio e confronti il prezzo con Amazon. Senza registrazione.',
  'Scanner per <em>codici a barre</em>, gratis',
  '''<p class="lead">BoomFlashnBuy è uno scanner per codici a barre pensato per una cosa sola: capire in un lampo se il prezzo che vedi in negozio è buono.</p>
[[VIDEO]]<h2>Cosa fa</h2><ul><li>Legge i codici <b>EAN-13, EAN-8, UPC</b> e altri formati comuni, anche storti o lontani.</li><li>Riconosce il prodotto e prepara la ricerca su Amazon nel <b>reparto giusto</b>.</li><li>Se il codice non c'è, dopo 5 secondi ti propone di <b>leggere l'etichetta</b>.</li><li>Funziona in <b>6 lingue</b> e usa l'Amazon del tuo Paese.</li></ul>
<h2>Come si usa</h2>''' + CTA_STEPS + '''
<h2>Privacy</h2><p>La fotocamera viene usata solo per leggere il codice, dentro l'app. Ricerche e spese restano sul tuo telefono: non serve un account.</p>''',
  [('Funziona su iPhone e Android?', 'Sì. Su iPhone si apre da Safari (e con “Ehi Siri: boom!”), su Android da Chrome, dove puoi anche installarla con un tocco.'),
   ('Perché il codice non viene letto?', 'Avvicina il telefono, evita i riflessi e accendi la torcia dall’icona 🔦. Se proprio non va, usa “Leggi l’etichetta”.')]),
 ('/guide/black-friday-prezzi/', 'Black Friday 2026: come capire se l’offerta in negozio conviene davvero',
  'Black Friday 2026 è venerdì 27 novembre. Prima di comprare in negozio, scansiona il codice a barre e confronta il prezzo con Amazon in pochi secondi.',
  'Black Friday: l’offerta <em>conviene davvero?</em>',
  '''<p class="lead">Il Black Friday 2026 cade <b>venerdì 27 novembre</b>, e il Cyber Monday lunedì 30. Nei negozi i cartelli “sconto” sono ovunque: il modo più veloce per capire se il prezzo è davvero buono è confrontarlo subito con Amazon, prodotto per prodotto.</p>
[[VIDEO]]<h2>In negozio, in 4 passi</h2>''' + CTA_STEPS + '''
<h2>3 consigli veloci</h2><ol><li><b>Confronta lo stesso prodotto</b>: il codice a barre evita di confondere modelli e formati simili.</li><li><b>Guarda il prezzo finale</b>, non la percentuale di sconto.</li><li><b>Tieni il conto</b>: scrivi il prezzo del negozio e vedi quanto risparmi in tutto.</li></ol>
<p>Nella sezione <b>Scopri</b> dell'app trovi anche le ricerche pronte per le offerte del momento.</p>''',
  [('Quando è il Black Friday 2026?', 'Venerdì 27 novembre 2026. Il Cyber Monday è lunedì 30 novembre 2026.'),
   ('L’app mostra il prezzo Amazon direttamente?', 'Apre Amazon con la ricerca già pronta per quel prodotto, dove vedi tutte le offerte e i venditori.')]),
 ('/guide/ehi-siri-boom/', '“Ehi Siri: boom!” Apri lo scanner prezzi con la voce (e su Android con un tocco)',
  'Come aprire lo scanner per codici a barre di BoomFlashnBuy con Siri su iPhone, o tenendo premuta l’icona su Android.',
  '“Ehi Siri: <em>boom!</em>”',
  '''<p class="lead">In negozio hai le mani occupate. Con un comando vocale lo scanner si apre da solo, pronto a leggere il codice.</p>
[[VIDEO]]<h2>Su iPhone</h2><ol><li>Apri <a href="/">BoomFlashnBuy</a> da Safari: alla prima apertura compare “Ehi Siri: boom!”.</li><li>Tocca <b>“＋ Aggiungi a Siri”</b> e conferma.</li><li>Da quel momento di' <b>“Ehi Siri: boom!”</b>, tutto di seguito: si apre lo scanner.</li></ol>
<h2>Su Android</h2><ol><li>Apri BoomFlashnBuy da Chrome e tocca <b>“Installa l’app”</b>.</li><li><b>Tieni premuta l'icona</b> dell'app sulla schermata del telefono e scegli <b>“BOOM! Scanner”</b>.</li></ol>''',
  [('Devo dire “Ehi Siri” e poi “boom”?', 'Puoi dirlo tutto di seguito: “Ehi Siri: boom!”.'),
   ('Posso spegnere i suoni?', 'Sì, con l’altoparlante in alto nell’app: grigio sbarrato vuol dire muto.')]),
]

def write(rel, txt):
    p = os.path.join(ROOT, rel.lstrip('/'))
    os.makedirs(os.path.dirname(p), exist_ok=True); open(p, 'w').write(txt)

for slug, title, desc, h1, body, faq in PAGES:
    write(slug + 'index.html', page(slug, title, desc, h1, body, faq))
# pagina video
write('/video/index.html', page('/video/', 'Video: BoomFlashnBuy in 30 secondi', 'Guarda come funziona BoomFlashnBuy: scansioni il codice a barre in negozio e confronti il prezzo con Amazon in un lampo.',
  'BoomFlashnBuy <em>in 30 secondi</em>', '''[[VIDEO]]<p class="lead">Scansioni il codice a barre, scrivi il prezzo del negozio, tocchi “Trovato! Vai ai prezzi” e su Amazon trovi tutte le offerte. Lo scanner si apre anche con “Ehi Siri: boom!”, e puoi cercare a voce, fare liste e trovare idee regalo.</p>
<p>Formato verticale per il telefono: <a href="''' + VIDEO_V + '''">scarica il video verticale</a>.</p>'''))
# guide index
write('/guide/index.html', page('/guide/', 'Guide BoomFlashnBuy: confrontare i prezzi tra negozio e Amazon', 'Guide pratiche per risparmiare: confrontare prezzi in negozio e su Amazon, scanner codici a barre, Black Friday.',
  'Le <em>guide</em>', '<p class="lead">Consigli pratici per spendere meno, in pochi secondi.</p>[[VIDEO]]', video=True))
# sitemap con video
urls = ['/', '/video/', '/guide/'] + [p[0] for p in PAGES]
def vtag(u):
    if u == '/': return ''
    return (f'<video:video><video:thumbnail_loc>{BASE}{POSTER}</video:thumbnail_loc><video:title>{html.escape(VIDEO_LD["name"])}</video:title>'
            f'<video:description>{html.escape(VIDEO_LD["description"])}</video:description><video:content_loc>{BASE}{VIDEO}</video:content_loc><video:duration>64</video:duration></video:video>')
sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:video="http://www.google.com/schemas/sitemap-video/1.1">\n' + \
     ''.join(f'<url><loc>{BASE}{u}</loc><lastmod>{TODAY}</lastmod>{vtag(u)}</url>\n' for u in urls) + '</urlset>\n'
write('/sitemap.xml', sm)
write('/robots.txt', f'User-agent: *\nAllow: /\nDisallow: /api/\n\nSitemap: {BASE}/sitemap.xml\n')
ix = os.path.join(ROOT, 'index.html'); t = open(ix).read(); bf = os.path.join(ROOT, 'tools', 'base.txt')
old = open(bf).read().strip() if os.path.exists(bf) else '__BASE__'
t = t.replace(old + '/', BASE + '/'); open(ix, 'w').write(t); open(bf, 'w').write(BASE)
print('ok', BASE, len(urls), 'pagine')

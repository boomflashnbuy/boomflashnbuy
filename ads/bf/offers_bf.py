"""Schermata 'Offerte online' per lo spot Black Friday (stile app, come ads/duo). uso: python3 offers_bf.py it|en|es"""
import asyncio, sys, os
from playwright.async_api import async_playwright
D = os.path.dirname(os.path.abspath(__file__))
L = {
 'it': dict(t='Offerte online', st='In negozio', best='Il prezzo più basso', sel='Venditore', sh='Consegna gratuita',
            n='Friggitrice ad aria digitale 5,5 L', sv='−50 € rispetto al negozio · spedizione inclusa', f=lambda v: f'€ {v}'),
 'en': dict(t='Online offers', st='In store', best='Lowest price', sel='Seller', sh='Free delivery',
            n='Digital air fryer 5.5 L', sv='€50 less than in store · delivery included', f=lambda v: f'€{v}'),
 'es': dict(t='Ofertas online', st='En tienda', best='El precio más bajo', sel='Vendedor', sh='Envío gratis',
            n='Freidora de aire digital 5,5 L', sv='−50 € respecto a la tienda · envío incluido', f=lambda v: f'{v} €'),
}
CSS = """*{box-sizing:border-box;margin:0}body{background:#0B0C0A;color:#fff;font-family:Sora,system-ui,sans-serif;padding:22px 18px;width:390px;height:844px;overflow:hidden}
@font-face{font-family:Sora;src:url(ttf/sora_var.ttf)}@font-face{font-family:Exo;src:url(ttf/exo_var_i.ttf);font-style:italic}
.hd{display:flex;align-items:center;gap:10px;margin:30px 0 12px}.hd img{width:30px;height:30px;border-radius:50%}.hd b{font:900 italic 24px Exo;color:#D4FF4A}
.pr{font-weight:700;font-size:17px;margin-bottom:12px}.chip{display:inline-block;background:#1b1e18;border-radius:12px;padding:8px 12px;font-size:14px;color:#cfd3c6;margin-bottom:16px}
.chip s{color:#ff6b6b;margin-left:6px;font-weight:700}
.o{display:flex;gap:12px;background:#151812;border:1.5px solid #262a24;border-radius:20px;padding:12px;margin-bottom:12px;align-items:center}
.o.best{border-color:#D4FF4A;box-shadow:0 0 24px rgba(212,255,74,.25)}
.im{width:88px;height:88px;border-radius:14px;background:#fff center/cover no-repeat;flex:none}
.bg{display:inline-block;background:#D4FF4A;color:#0B0C0A;font-size:11px;font-weight:800;border-radius:8px;padding:3px 8px;margin-bottom:4px}
.nm{font-weight:700;font-size:14px}.sh{font-size:11px;color:#8f958a;margin:2px 0 4px}.pc{font:800 30px Sora}.svl{color:#D4FF4A;font-size:12px;font-weight:700}"""
def page(lg):
    d = L[lg]; f = d['f']
    def card(p, i, best=False):
        b = f'<div class="bg">{d["best"]}</div>' if best else ''
        s = f'<div class="svl">{d["sv"]}</div>' if best else ''
        return f'<div class="o{" best" if best else ""}"><div class="im" style="background-image:url(fryer.jpg)"></div><div>{b}<div class="nm">{d["n"]}</div><div class="sh">{d["sel"]} {"ABC"[i]} · {d["sh"]}</div><div class="pc">{f(p)}</div>{s}</div></div>'
    return f'<!doctype html><meta charset="utf-8"><style>{CSS}</style><div class="hd"><img src="logo.png"><b>{d["t"]}</b></div><div class="pr">{d["n"]}</div><div class="chip">{d["st"]} <s>{f(179)}</s></div>{card(129,0,True)}{card(139,1)}{card(149,2)}'
async def main(lg):
    os.makedirs(f'{D}/app', exist_ok=True)
    h = f'{D}/app/off_{lg}.html'; open(h, 'w').write(page(lg).replace('url(ttf', f'url({D}/ttf').replace('url(fryer', f'url({D}/fryer').replace('src="logo', f'src="{D}/logo'))
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(viewport={'width': 390, 'height': 844}, device_scale_factor=3)
        await pg.goto('file://' + h); await pg.wait_for_timeout(700); await pg.screenshot(path=f'{D}/app/off_{lg}.png'); await b.close()
for lg in sys.argv[1:]: asyncio.run(main(lg))

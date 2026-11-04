"""Carosello IG "Indovina il prezzo" (EN/ES), 1080x1350, palette brand nero/lime."""
import json, sys
from pathlib import Path
from playwright.sync_api import sync_playwright

HERE = Path(__file__).parent
T = json.loads((HERE / "texts.json").read_text())

CSS = """
@font-face{font-family:Exo2;font-weight:900;font-style:italic;src:url(exo.woff2)}
@font-face{font-family:Sora;font-weight:800;src:url(sora8.woff2),url(sora8x.woff2)}
@font-face{font-family:Sora;font-weight:700;src:url(sora7.woff2),url(sora7x.woff2)}
*{margin:0;box-sizing:border-box}
body{width:1080px;height:1350px;background:radial-gradient(120% 80% at 50% 0%,#262A24 0%,#0B0C0A 62%);
 color:#fff;font-family:Sora;font-weight:700;overflow:hidden;position:relative}
.top{position:absolute;top:56px;left:64px;right:64px;display:flex;justify-content:space-between;align-items:center}
.pill{border:3px solid #D4FF4A;color:#D4FF4A;border-radius:999px;padding:10px 26px;font-size:30px;letter-spacing:2px;font-weight:800}
.logo{width:110px;height:110px}
h1{font-family:Exo2;font-weight:900;font-style:italic;font-size:104px;line-height:.95;text-transform:uppercase;
 position:absolute;left:64px;right:64px;top:200px}
h1 em{color:#D4FF4A;font-style:italic}
.sub{position:absolute;left:64px;right:64px;font-size:42px;line-height:1.3;color:#e8e8e8}
.card{position:absolute;left:50%;transform:translateX(-50%);width:600px;height:600px;border-radius:44px;background:#fff;
 overflow:hidden;box-shadow:0 0 0 4px #D4FF4A33,0 30px 80px #000a}
.card img{width:100%;height:100%;object-fit:cover}
.tag{position:absolute;font-family:Exo2;font-weight:900;font-style:italic;border-radius:22px;padding:14px 28px}
.store{background:#fff;color:#0B0C0A;font-size:64px}
.amz{background:#D4FF4A;color:#0B0C0A;font-size:64px}
.q{background:#0B0C0A;color:#D4FF4A;border:4px solid #D4FF4A;font-size:120px;padding:0 44px}
.save{position:absolute;left:0;right:0;text-align:center;font-family:Exo2;font-weight:900;font-style:italic;
 font-size:150px;color:#D4FF4A;text-shadow:0 0 40px #D4FF4A66}
.foot{position:absolute;bottom:52px;left:64px;right:64px;display:flex;justify-content:space-between;font-size:28px;color:#9a9f95}
.swipe{color:#D4FF4A;font-weight:800}
.cta{position:absolute;left:64px;right:64px;top:480px;font-size:46px;line-height:1.35}
.cta b{color:#D4FF4A}
.btn{position:absolute;left:64px;right:64px;top:920px;background:#D4FF4A;color:#0B0C0A;border-radius:28px;text-align:center;
 padding:34px 0;font-family:Exo2;font-weight:900;font-style:italic;font-size:62px}
.send{position:absolute;left:64px;right:64px;top:1080px;text-align:center;font-size:36px;color:#fff}
"""

def page(body, n, t):
    swipe = f'<span class="swipe">{t["swipe"]}</span>' if n < 5 else '<span></span>'
    return f"""<html><head><style>{CSS}</style></head><body>
<div class="top"><div class="pill">{t['pill']} · {n}/5</div><img class="logo" src="logo.png"></div>
{body}
<div class="foot"><span>{t['example']}</span>{swipe}</div></body></html>"""

def slides(t):
    s = []
    # 1 domanda borsa
    s.append(f"""<h1>{t['h1a']}<br><em>{t['h1b']}</em></h1>
<div class="card" style="top:480px"><img src="prod_bag.jpg"></div>
<div class="tag store" style="top:470px;left:150px">{t['store']} {t['p'](199)}</div>
<div class="tag q" style="top:900px;right:150px">?</div>
<div class="sub" style="top:1130px;text-align:center">{t['ask']}</div>""")
    # 2 svela borsa
    s.append(f"""<h1>{t['r1a']}<br><em>{t['r1b']}</em></h1>
<div class="card" style="top:430px;width:480px;height:480px"><img src="prod_bag.jpg"></div>
<div class="tag store" style="top:420px;left:170px;text-decoration:line-through">{t['p'](199)}</div>
<div class="tag amz" style="top:840px;right:170px">Amazon {t['p'](139)}</div>
<div class="save" style="top:960px">−{t['p'](60)}</div>""")
    # 3 domanda monopattino
    s.append(f"""<h1>{t['h2a']}<br><em>{t['h2b']}</em></h1>
<div class="card" style="top:480px"><img src="prod_sc.jpg"></div>
<div class="tag store" style="top:470px;left:150px">{t['store']} {t['p'](299)}</div>
<div class="tag q" style="top:900px;right:150px">?</div>
<div class="sub" style="top:1130px;text-align:center">{t['ask2']}</div>""")
    # 4 svela monopattino
    s.append(f"""<h1>{t['r2a']}<br><em>{t['r2b']}</em></h1>
<div class="card" style="top:430px;width:480px;height:480px"><img src="prod_sc.jpg"></div>
<div class="tag store" style="top:420px;left:170px;text-decoration:line-through">{t['p'](299)}</div>
<div class="tag amz" style="top:840px;right:170px">Amazon {t['p'](249)}</div>
<div class="save" style="top:960px">−{t['p'](50)}</div>""")
    # 5 CTA
    s.append(f"""<h1>{t['c1']}<br><em>{t['c2']}</em></h1>
<div class="cta">{t['cta']}</div>
<div class="btn">{t['btn']}</div>
<div class="send">{t['send']}</div>""")
    return s

def main():
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 1080, "height": 1350}, device_scale_factor=1)
        for lang, t in T.items():
            fmt = t.pop("fmt")
            t["p"] = (lambda v, f=fmt: f.format(v))
            for i, html in enumerate(slides(t), 1):
                f = HERE / f"_tmp.html"
                f.write_text(page(html, i, t))
                pg.goto(f.resolve().as_uri())
                pg.wait_for_timeout(300)
                out = HERE / "out" / f"guess-{lang}-{i}.jpg"
                out.parent.mkdir(exist_ok=True)
                pg.screenshot(path=str(out), type="jpeg", quality=90)
                print(out)
        b.close()

if __name__ == "__main__":
    main()

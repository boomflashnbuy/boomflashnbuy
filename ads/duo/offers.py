import asyncio,sys,importlib.util
sys.path.insert(0,'/home/claude/ads/offersw')
spec=importlib.util.spec_from_file_location('g','/home/claude/ads/offersw/gen.py')
src=open('/home/claude/ads/offersw/gen.py').read().split('async def main')[0]
ns={};exec(src,ns);L=ns['L'];CSS=ns['CSS']
from playwright.async_api import async_playwright
P={'it':{'bag':('Borsa a mano in pelle nera','−60 € rispetto al negozio · spedizione inclusa'),'sc':('Monopattino elettrico pieghevole','−50 € rispetto al negozio · spedizione inclusa')}}
IM={'bag':[('/home/claude/ads/duo/th_bag0.jpg','50% 50%',100),('/home/claude/ads/duo/th_bag1.jpg','50% 50%',100),('/home/claude/ads/duo/th_bag2.jpg','50% 50%',100)],'sc':[('/home/claude/ads/duo/th_sc0.jpg','50% 50%',100),('/home/claude/ads/duo/th_sc1.jpg','50% 50%',100),('/home/claude/ads/duo/th_sc2.jpg','50% 50%',100)]}
PR={'bag':(199,[139,149,159]),'sc':(299,[249,269,279])}
def page(lg,k):
    d=L[lg];f=d['f'];name,sv=P[lg][k];st,ps=PR[k]
    def card(i,n,best=False):
        img,pos,sz=IM[k][i]
        extra=f'<div class="bg">{d["best"]}</div>' if best else ''
        svl=f'<div class="svl">{sv}</div>' if best else ''
        return f'<div class="o{" best" if best else ""}"><div class="im" style="background-image:url({img});background-position:{pos};background-size:{sz}%"></div><div class="tx">{extra}<div class="nm">{name}</div><div class="sh">{d["sel"]} {"ABC"[i]} · {d["sh"]}</div><div class="pc">{f(n)}</div>{svl}</div></div>'
    return f'<!doctype html><meta charset="utf-8"><base href="file:///home/claude/ads/offersw/"><style>{CSS}</style><div class="hd"><img src="../logo.png"><b>{d["t"]}</b></div><div class="pr">{name}</div><div class="chip">{d["st"]} <s>{f(st)}</s></div>{card(0,ps[0],True)}{card(1,ps[1])}{card(2,ps[2])}<div class="ft">{d["ft"]}</div>'
async def main(lg):
    async with async_playwright() as p:
        b=await p.chromium.launch();pg=await b.new_page(viewport={'width':390,'height':844},device_scale_factor=3)
        for k in ['bag','sc']:
            h=page(lg,k).replace('url(../QA','url(/home/claude/ads/duo/QA').replace('url(../PB','url(/home/claude/ads/duo/PB')
            open(f'app/{lg}/off_{k}.html','w').write(h)
            await pg.goto(f'file:///home/claude/ads/duo/app/{lg}/off_{k}.html');await pg.wait_for_timeout(600)
            await pg.screenshot(path=f'app/{lg}/off_{k}.png')
        await b.close()
asyncio.run(main(sys.argv[1]))

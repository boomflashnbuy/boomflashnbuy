import asyncio,subprocess,json,time,sys,os
from playwright.async_api import async_playwright
S='/tmp/claude-0/-home-claude/a9e628dc-c99c-5755-be64-a3532a4dd769/scratchpad'
IOS='Mozilla/5.0 (iPhone; CPU iPhone OS 26_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/26.0 Mobile/15E148 Safari/604.1'
LOC={'it':'it-IT','en':'en-GB','es':'es-ES','fr':'fr-FR','de':'de-DE','pt':'pt-PT'}
Q={'it':'cuffie bluetooth sotto 50 euro','en':'bluetooth headphones under 50 pounds','es':'auriculares bluetooth menos de 50 euros','fr':'casque bluetooth moins de 50 euros','de':'Bluetooth Kopfhörer unter 50 Euro','pt':'auscultadores bluetooth até 50 euros'}
srv=subprocess.Popen(['python3','-m','http.server','8819','-d','/home/claude/saynbuy'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
async def mk(p,cam,lg,noread=False):
  b=await p.chromium.launch(args=['--use-fake-ui-for-media-stream','--use-fake-device-for-media-stream',f'--use-file-for-fake-video-capture={S}/scan2/cams/{cam}.y4m'])
  ctx=await b.new_context(viewport={'width':390,'height':844},device_scale_factor=2,user_agent=IOS,is_mobile=True,has_touch=True,locale=LOC[lg],permissions=['camera','microphone'])
  await ctx.add_init_script("window.__noBD=true;try{localStorage.setItem('snb-siri-seen','1');localStorage.setItem('snb-bk','9')}catch(e){}")
  async def off(r):
    u=r.request.url
    if 'upc' in u: await r.fulfill(status=200,content_type='application/json',body=json.dumps({"code":"OK","items":[{"title":"Apple AirPods 4","brand":"Apple","images":[]}]}))
    else: await r.fulfill(status=200,content_type='application/json',body='{"status":0}')
  await ctx.route(lambda u: any(h in u for h in ['facts.org','upcitemdb','/api/upc']),off)
  await ctx.route('**/*amazon.*/**',lambda r:r.fulfill(status=200,body='AMZ'))
  if noread: await ctx.add_init_script("window.ZXingWASM=new Proxy({},{get:(t,k)=>k==='then'?undefined:(async()=>[])})")
  return b,ctx
async def main(lg):
  T=f'{S}/rv/{lg}/';os.makedirs(T,exist_ok=True);meta={}
  async def sh(pg,n):await pg.wait_for_timeout(450);await pg.screenshot(path=T+n+'.png')
  async with async_playwright() as p:
    b,ctx=await mk(p,'s13_airpods',lg,True);pg=await ctx.new_page();await pg.goto('http://localhost:8819/?boom=1');await pg.wait_for_timeout(2200)
    await pg.evaluate("document.querySelectorAll('.bm-laser').forEach(x=>x.style.visibility='hidden');const w=document.getElementById('bmw0');w.style.animation='none';w.style.opacity='1'");await sh(pg,'scan')
    await pg.evaluate("document.getElementById('bmw0').style.opacity='.22'");await sh(pg,'scan_dim')
    meta['frame']=await pg.evaluate("(()=>{const r=document.querySelector('.bm-frame').getBoundingClientRect();return [r.x,r.y,r.width,r.height]})()")
    meta['boomw']=await pg.evaluate("(()=>{const r=document.querySelector('#bmw0').getBoundingClientRect();return [r.x,r.y,r.width,r.height]})()")
    await b.close()
    b,ctx=await mk(p,'s13_airpods',lg);pg=await ctx.new_page();await pg.goto('http://localhost:8819/?boom=1')
    await pg.wait_for_function("document.getElementById('bmbtn').classList.contains('found')&&!document.getElementById('bmw')",timeout=15000)
    await pg.fill('#bmsp','149');await pg.evaluate("document.activeElement.blur()");await sh(pg,'found')
    meta['btn']=await pg.evaluate("(()=>{const r=document.querySelector('#bmbtn').getBoundingClientRect();return [r.x,r.y,r.width,r.height]})()")
    meta['card']=await pg.evaluate("(()=>{const r=document.querySelector('#bmcard').getBoundingClientRect();return [r.x,r.y,r.width,r.height]})()")
    await pg.goto('http://localhost:8819/');await pg.wait_for_timeout(800)
    await pg.evaluate("s=>{localStorage.setItem('snb-save',JSON.stringify(s))}",[{"t":int(time.time()*1000),"n":"AirPods 4","store":149,"amz":109}])
    await pg.evaluate("home()");await sh(pg,'home_save')
    meta['savec']=await pg.evaluate("(()=>{const r=document.querySelector('.savec').getBoundingClientRect();return [r.x,r.y,r.width,r.height]})()")
    await pg.evaluate("localStorage.removeItem('snb-save');home()");await sh(pg,'home')
    meta['mic']=await pg.evaluate("(()=>{const r=document.querySelector('#bm').getBoundingClientRect();return [r.x,r.y,r.width,r.height]})()")
    meta['scn']=await pg.evaluate("(()=>{const r=document.querySelector('#scn').getBoundingClientRect();return [r.x,r.y,r.width,r.height]})()")
    await pg.evaluate(f"""document.body.classList.add('listening');document.getElementById('mic').classList.add('on');document.getElementById('q').value={json.dumps(Q[lg])}""");await sh(pg,'voice')
    await pg.evaluate("document.body.classList.remove('listening');document.getElementById('mic').classList.remove('on')")
    await pg.fill('#q',Q[lg]);await pg.click('#go',force=True);await sh(pg,'result')
    await pg.evaluate("home()");await pg.evaluate("$('#q').value=LS[lang].listEx;run()");await sh(pg,'list')
    await pg.evaluate("home()");await pg.evaluate("$('#q').value=NX[lang].probEx;run()");await sh(pg,'problem')
    await pg.evaluate("home()");await pg.click('#gw',force=True);await sh(pg,'gift')
    json.dump(meta,open(T+'meta.json','w'));await b.close()
try:
  for lg in sys.argv[1:]: asyncio.run(main(lg))
finally: srv.kill()

import asyncio,subprocess,json,sys,time,base64
from playwright.async_api import async_playwright
lg=sys.argv[1]
NM={'it':('Borsa in pelle nera','Monopattino elettrico')}
LOC={'it':'it-IT','en':'en-IE','es':'es-ES','fr':'fr-FR','de':'de-DE','pt':'pt-PT'}
srv=subprocess.Popen(['python3','-m','http.server','8825','-d','/home/claude/seo'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL);time.sleep(1)
async def main():
  async with async_playwright() as p:
    for key,(n,st,am) in {'bag':(NM[lg][0],199,139),'sc':(NM[lg][1],299,249)}.items():
      b=await p.chromium.launch();ctx=await b.new_context(viewport={'width':390,'height':844},device_scale_factor=3,locale=LOC[lg])
      now=int(time.time()*1000)
      await ctx.add_init_script(f"try{{localStorage.setItem('snb-bk','9');localStorage.setItem('snb-lang','{lg}');localStorage.setItem('snb-save',{json.dumps(json.dumps([{'t':now,'n':n,'store':st,'amz':am}]))});localStorage.setItem('snb-siri-seen','1')}}catch(e){{}}")
      pg=await ctx.new_page();await pg.goto(f'http://localhost:8825/?lang={lg}');await pg.wait_for_timeout(1500)
      data=await pg.evaluate("(async()=>{last={n:"+json.dumps(n)+",store:"+str(st)+",amz:"+str(am)+"};const b=await cardImg();return await new Promise(r=>{const f=new FileReader();f.onload=()=>r(f.result);f.readAsDataURL(b)})})()")
      open(f'app/{lg}/card_{key}.png','wb').write(base64.b64decode(data.split(',')[1]));await b.close()
try: asyncio.run(main())
finally: srv.kill()

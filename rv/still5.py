import asyncio,subprocess,sys,json
from playwright.async_api import async_playwright
d='/tmp/claude-0/-home-claude/a9e628dc-c99c-5755-be64-a3532a4dd769/scratchpad/'
lg,f,dv=sys.argv[1],sys.argv[2],sys.argv[3];ts=[float(x) for x in sys.argv[4:]]
srv=subprocess.Popen(['python3','-m','http.server','8811','--bind','127.0.0.1'],cwd=d,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch();W,H=(1080,1920) if f=='v' else (1920,1080)
    pg=await b.new_page(viewport={'width':W,'height':H});errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
    await pg.goto(f'http://127.0.0.1:8811/rv/stage5.html?lang={lg}&f={f}&d={dv}');await pg.evaluate('ready');await pg.evaluate('m=>setMeta(m)',json.load(open(d+f'rv/{lg}/meta.json')))
    for t in ts:
      await pg.evaluate(f'render({t})');await pg.screenshot(path=d+f'rv/st_{dv}{f}_{t}.jpg',type='jpeg',quality=80)
    print(errs);await b.close()
try: asyncio.run(m())
finally: srv.terminate()

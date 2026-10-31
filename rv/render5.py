import asyncio,subprocess,sys,json,os
from playwright.async_api import async_playwright
d='/tmp/claude-0/-home-claude/a9e628dc-c99c-5755-be64-a3532a4dd769/scratchpad/'
lg=sys.argv[1];DV=sys.argv[2];FMTS=sys.argv[3:] or ['v','h']
SC=[(0,3.2),(3.2,7.2),(7.2,10),(10,20.6),(20.6,24.6),(24.6,28.2),(28.2,34)]
FPS=30
NAME={'v':'verticale','h':'orizzontale'};DN={'ios':'iPhone','and':'Android','both':'video'}
async def m():
  async with async_playwright() as p:
    b=await p.chromium.launch()
    for f in FMTS:
      W,H=(1080,1920) if f=='v' else (1920,1080)
      pg=await b.new_page(viewport={'width':W,'height':H})
      await pg.goto(f'http://127.0.0.1:8814/rv/stage5.html?lang={lg}&f={f}&d={DV}');await pg.evaluate('ready');await pg.evaluate('m=>setMeta(m)',json.load(open(d+f'rv/{lg}/meta.json')))
      od=d+f'rv/out5/{lg}_{DV}_{f}/';os.makedirs(od,exist_ok=True);parts=[]
      for si,(a,e) in enumerate(SC):
        fn=od+f's{si}.mp4';parts.append(fn)
        if os.path.exists(fn): continue
        tmp=od+f's{si}.tmp.mp4'
        ff=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','image2pipe','-framerate',str(FPS),'-c:v','mjpeg','-i','-','-c:v','libx264','-preset','medium','-crf','18','-pix_fmt','yuv420p','-r',str(FPS),tmp],stdin=subprocess.PIPE)
        for i in range(round(a*FPS),round(e*FPS)):
          await pg.evaluate(f'render({i/FPS})')
          ff.stdin.write(await pg.screenshot(type='jpeg',quality=92))
        ff.stdin.close();rc=ff.wait()
        if rc==0: os.rename(tmp,fn)
        else: raise SystemExit('ffmpeg fail')
      open(od+'list.txt','w').write(''.join(f"file '{x}'\n" for x in parts))
      os.makedirs(d+'rv/final',exist_ok=True);out=d+f'rv/final/BoomFlashnBuy-{lg}-{NAME[f]}.mp4'
      subprocess.run(['ffmpeg','-y','-loglevel','error','-f','concat','-safe','0','-i',od+'list.txt','-i',d+'rv/mix34.wav','-map','0:v','-map','1:a','-c:v','copy','-c:a','aac','-b:a','192k','-shortest','-movflags','+faststart',out],check=True)
      await pg.close();print('done',out,flush=True)
    await b.close()
asyncio.run(m())

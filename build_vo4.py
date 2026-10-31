import sys,subprocess,numpy as np,soundfile as sf,json
from PIL import Image
D='/tmp/claude-0/-home-claude/a9e628dc-c99c-5755-be64-a3532a4dd769/scratchpad/'
lg,f,out=sys.argv[1],sys.argv[2],sys.argv[3]
VDIR=sys.argv[4] if len(sys.argv)>4 else 'mac'
SR=48000;FPS=30;X=0.5;LEAD=0.35
def load(p):
    a,sr=sf.read(p,always_2d=True);a=a.mean(1)
    if sr!=SR:
        n=int(len(a)*SR/sr);a=np.interp(np.linspace(0,len(a)-1,n),np.arange(len(a)),a)
    return a
vo=[load(D+f'{VDIR}/{lg}/frase{i}.wav') for i in range(1,12)]
INTRO=float(__import__('os').environ.get('INTRO','0'))
dur=[max(3.0,len(v)/SR+LEAD+0.95) for v in vo];dur[-1]+=1.6;dur[0]+=INTRO
S=np.concatenate([[0],np.cumsum(dur)]);T=S[-1];N=int(T*SR)
# musica stereo: estesa ripetendo il centro, finale originale allineato alla fine
import os
ms,msr=sf.read(D+'rv/base_eq.wav',always_2d=True)
def ext(m):
    L=len(m)/SR
    if T>L:
        cut=18.0;xf=int(1.0*SR);r=np.linspace(0,1,xf)
        def xjoin(x,y):
            z=x.copy();z[-xf:]=x[-xf:]*(1-r)+y[:xf]*r;return np.concatenate([z,y[xf:]])
        tail=m[int(cut*SR)-xf:];need=int(T*SR)-len(tail)+xf
        body=m[:int(cut*SR)]
        while len(body)<need: body=xjoin(body,m[int(6*SR):int(cut*SR)])
        body=body[:need];m=xjoin(body,tail)
    return np.pad(m,(0,max(0,N-len(m))))[:N]
M=np.stack([ext(ms[:,0]),ext(ms[:,1])],1)
voc=np.zeros(N)
for i,v in enumerate(vo):
    s=int((S[i]+LEAD+(INTRO if i==0 else 0))*SR);voc[s:s+len(v)]+=v[:N-s]
fx=np.zeros(N)
def put(p,t,g):
    a=load(p);s=int(t*SR);n=min(len(a),N-s);fx[s:s+n]+=a[:n]*g
rng=np.random.default_rng(3);wl=int(.45*SR);w=rng.standard_normal(wl)
from scipy.signal import lfilter
w=lfilter([0.06],[1,-0.94],w);w*=np.sin(np.linspace(0,np.pi,wl))**2;w/=np.abs(w).max()
for i in range(1,11):
    s0=int((S[i]-0.3)*SR);fx[s0:s0+wl]+=w*0.10
put(D+'snd/beep.wav',S[4]+0.05,0.55)
put(D+'snd/kaching.wav',S[5]+LEAD+len(vo[5])/SR+0.15,0.5)
sf.write(out+'_m.wav',M,SR);sf.write(out+'_v.wav',voc,SR);sf.write(out+'_fx.wav',fx,SR)
MUS=os.environ.get('MUS','0.75');VOX=os.environ.get('VOX','1.0');THR=os.environ.get('THR','0.03');RAT=os.environ.get('RAT','6');REL=os.environ.get('REL','650')
fc=(f"[1:a]aformat=channel_layouts=mono,asplit=2[vk][vv];"
    f"[0:a]volume={MUS}[mm];[vk]aformat=channel_layouts=stereo[vks];"
    f"[mm][vks]sidechaincompress=threshold={THR}:ratio={RAT}:attack=40:release={REL}:knee=4:makeup=1[md];"
    f"[vv]volume={VOX},aformat=channel_layouts=stereo[vs];[2:a]aformat=channel_layouts=stereo[fs];"
    f"[md][vs][fs]amix=inputs=3:normalize=0[bus];"
    f"[bus]acompressor=threshold=-16dB:ratio=2:attack=25:release=250:makeup=1.5,alimiter=limit=0.89:attack=3:release=60[o]")
subprocess.run(['ffmpeg','-v','error','-y','-i',out+'_m.wav','-i',out+'_v.wav','-i',out+'_fx.wav','-filter_complex',fc,'-map','[o]','-ar','48000',out+'.wav'],check=True)
# video
cards=[np.asarray(Image.open(D+f'rv/cards/{lg}/{f}/{i:02d}.jpg').convert('RGB'),dtype=np.float32) for i in range(1,12)]
H,W=cards[0].shape[:2]
p=subprocess.Popen(['ffmpeg','-y','-loglevel','error','-f','rawvideo','-pix_fmt','rgb24','-s',f'{W}x{H}','-r',str(FPS),'-i','-','-i',out+'.wav',
  '-af','loudnorm=I=-14:TP=-1.5:LRA=9','-c:v','libx264','-preset','medium','-crf','18','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-ar','48000','-movflags','+faststart','-shortest',out+'.mp4'],stdin=subprocess.PIPE)
nf=int(round(T*FPS))
for k in range(nf):
    t=k/FPS;i=int(np.searchsorted(S,t,side='right')-1);i=min(i,10)
    fr=cards[i]
    if i<10 and t>S[i+1]-X/2:
        u=(t-(S[i+1]-X/2))/X;u=u*u*(3-2*u);fr=cards[i]*(1-u)+cards[i+1]*u
    elif i>0 and t<S[i]+X/2:
        u=(t-(S[i]-X/2))/X;u=u*u*(3-2*u);fr=cards[i-1]*(1-u)+cards[i]*u
    if k==nf-1 or True: pass
    p.stdin.write(fr.astype(np.uint8).tobytes())
p.stdin.close();p.wait()
json.dump({'S':list(map(float,S)),'T':float(T)},open(out+'.json','w'))
print(lg,f,round(T,2))

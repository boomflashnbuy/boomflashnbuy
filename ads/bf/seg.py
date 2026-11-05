import sys, soundfile as sf, numpy as np, subprocess
f=sys.argv[1]; lang=sys.argv[2]; gapmin=float(sys.argv[3]) if len(sys.argv)>3 else 0.3
x,sr=sf.read(f); fr=int(sr*0.01)
e=np.array([np.sqrt(np.mean(x[i:i+fr]**2)) for i in range(0,len(x)-fr,fr)]); on=e>0.008
segs=[];s=None;g=0
for i,v in enumerate(on):
    if v:
        if s is None: s=i
        g=0
    elif s is not None:
        g+=1
        if g*0.01>gapmin: segs.append((s*0.01,(i-g+1)*0.01)); s=None; g=0
if s is not None: segs.append((s*0.01,len(on)*0.01))
args=[f'{max(0,a-0.08):.2f}-{min(len(x)/sr,b+0.1):.2f}' for a,b in segs if b-a>0.15]
print(round(len(x)/sr,2)); subprocess.run(['python3','asr.py',lang,f]+args)

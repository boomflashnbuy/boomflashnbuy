import json,soundfile as sf,os,sys
from kokoro_onnx import Kokoro
K='/tmp/claude-0/-home-claude/a9e628dc-c99c-5755-be64-a3532a4dd769/scratchpad/kok/'
k=Kokoro(K+'kokoro-v1.0.onnx',K+'voices-v1.0.bin')
BR='bˈuːm flˈæʃ ænd bˈaɪ'
d=json.load(open('lines.json'));lg=sys.argv[1]
V={'G':'if_sara','L':'im_nicola','N':'im_nicola'}
os.makedirs(f'vo_{lg}',exist_ok=True);out=[]
for i,(shot,sp,t) in enumerate(d[lg],1):
    t2=t.replace('BoomFlashnBuy','Boom Flash and Buy')
    parts=t2.split('Boom Flash and Buy')
    if len(parts)>1:
        ph=(' '+BR+' ').join(k.tokenizer.phonemize(p,'it') if p.strip() else '' for p in parts)
        a,sr=k.create(ph.strip(),voice=V[sp],speed=1.05,lang='it',is_phonemes=True)
    else: a,sr=k.create(t2,voice=V[sp],speed=1.05 if sp!='N' else 1.0,lang='it')
    sf.write(f'vo_{lg}/{i}.wav',a,sr);out.append(round(len(a)/sr,2))
print(out)

import sys,soundfile as sf,numpy as np,os
from kokoro_onnx import Kokoro
k=Kokoro('kokoro-v1.0.onnx','voices-v1.0.bin')
T='/tmp/claude-0/-home-claude/a9e628dc-c99c-5755-be64-a3532a4dd769/scratchpad/txt2/'
B='bˈuːm flˈæʃ ænd bˈaɪ'
jobs={'en':('am_michael','en-us'),'es':('em_alex','es'),'pt':('pm_alex','pt-br'),'fr':('ff_siwis','fr-fr')}
for lg in sys.argv[1:]:
    v,code=jobs[lg];out=f'../kok2/{lg}';os.makedirs(out,exist_ok=True)
    for i,l in enumerate([x.strip() for x in open(T+lg+'.txt') if x.strip()],1):
        if 'Boom Flash and Buy' in l:
            a_,b_=l.split('Boom Flash and Buy',1)
            ph=(k.tokenizer.phonemize(a_,code) if a_.strip() else '')+' '+B+(k.tokenizer.phonemize(b_,code) if b_.strip() else '')
            a,sr=k.create(ph.strip(),voice=v,speed=1.05,lang=code,is_phonemes=True)
        else:
            a,sr=k.create(l,voice=v,speed=1.05,lang=code)
        sf.write(f'{out}/frase{i}.wav',a,sr)
    print(lg,'ok')

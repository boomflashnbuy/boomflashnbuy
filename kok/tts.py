import sys,soundfile as sf
from kokoro_onnx import Kokoro
k=Kokoro('kokoro-v1.0.onnx','voices-v1.0.bin')
lg,voice,code,src,out=sys.argv[1:6]
import os;os.makedirs(out,exist_ok=True)
for i,l in enumerate([x.strip() for x in open(src) if x.strip()],1):
    a,sr=k.create(l,voice=voice,speed=0.95,lang=code)
    sf.write(f'{out}/frase{i}.wav',a,sr);print(i,round(len(a)/sr,2))

import sys, soundfile as sf, numpy as np, sherpa_onnx
from scipy.signal import resample_poly
M='/tmp/sherpa-onnx-whisper-small/small-'
lang=sys.argv[1]
r=sherpa_onnx.OfflineRecognizer.from_whisper(encoder=M+'encoder.int8.onnx',decoder=M+'decoder.int8.onnx',tokens=M+'tokens.txt',language=lang,task='transcribe')
f=sys.argv[2]; x,sr=sf.read(f); x=x if x.ndim==1 else x.mean(1)
for seg in sys.argv[3:]:
    a,b=map(float,seg.split('-')); y=x[int(a*sr):int(b*sr)].astype(np.float32)
    y=resample_poly(y,16000,sr).astype(np.float32)
    s=r.create_stream(); s.accept_waveform(16000,y); r.decode_stream(s); print(seg,'|',s.result.text)

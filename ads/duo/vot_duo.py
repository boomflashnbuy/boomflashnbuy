import soundfile as sf,numpy as np,json,sys
from scipy.signal import resample_poly
lg=sys.argv[1];TL=json.load(open(f'timeline_{lg}.json'));SR=44100;o=np.zeros(int(SR*(TL['total']+.5)))
for st,n in TL['vo']:
    x,sr=sf.read(f'vo_{lg}/{n}.wav');x=x if x.ndim==1 else x.mean(1)
    if sr!=SR: x=resample_poly(x,SR,sr)
    i=int(st*SR);j=min(len(o),i+len(x));o[i:j]+=x[:j-i]
sf.write(f'vo_{lg}.wav',o,SR);print('ok')

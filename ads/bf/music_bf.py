"""Musica originale per lo spot Black Friday (derivata da quella de "La sfida"): funk-pop brillante 112 BPM (basso slap, clap, shaker, accordi tipo Rhodes, stab di fiati sintetici), drop sul BOOM."""
import numpy as np, json, sys
from scipy.signal import butter, sosfilt
from scipy.io import wavfile
LG = sys.argv[1]; import os; HERE=os.path.dirname(os.path.abspath(__file__)); TL = json.load(open(f'{HERE}/timeline_{LG}.json'))
SR = 44100; TOTAL = TL['total']; N = int(SR * (TOTAL + .8)); BOOM = TL['boom']
BPM = 118; B = 60 / BPM
L = np.zeros(N); R = np.zeros(N); rng = np.random.default_rng(11)
lp = lambda x, f: sosfilt(butter(2, f, 'low', fs=SR, output='sos'), x)
hp = lambda x, f: sosfilt(butter(2, f, 'high', fs=SR, output='sos'), x)
bp = lambda x, a, b: sosfilt(butter(2, [a, b], 'band', fs=SR, output='sos'), x)
mtof = lambda m: 440 * 2 ** ((m - 69) / 12)
def env(n, a=.004, d=.2): t = np.arange(n) / SR; return np.minimum(1, t / a) * np.exp(-t / d)
def add(sig, st, g=1., pan=0.):
    i = int(round(st * SR))
    if i >= N or i < 0: return
    j = min(N, i + len(sig)); s = sig[:j - i] * g; L[i:j] += s * (1 - pan); R[i:j] += s * (1 + pan)
def kick():
    n = int(.4 * SR); t = np.arange(n) / SR
    return np.tanh(np.sin(2 * np.pi * np.cumsum(50 + 110 * np.exp(-t * 35)) / SR) * np.exp(-t * 9) * 1.8)
def snare():
    n = int(.25 * SR); t = np.arange(n) / SR
    return (bp(rng.standard_normal(n), 1500, 7000) * np.exp(-t * 18) * .7 + np.sin(2 * np.pi * 190 * t) * np.exp(-t * 30) * .5)
def clap():
    n = int(.3 * SR); nz = bp(rng.standard_normal(n), 900, 6000); e = np.zeros(n)
    for k, o in enumerate([0, .01, .021]):
        i = int(o * SR); e[i:] += env(n - i, .001, .01 if k < 2 else .11)
    return nz * e * .7
def shaker():
    n = int(.09 * SR); return hp(rng.standard_normal(n), 6000) * env(n, .015, .03) * .22
def slap(m, d=.22):
    n = int(d * SR); t = np.arange(n) / SR; f = mtof(m)
    s = np.sin(2 * np.pi * f * t) + .5 * np.sin(4 * np.pi * f * t) * np.exp(-t * 25) + .25 * np.sign(np.sin(2 * np.pi * f * t)) * np.exp(-t * 40)
    return lp(s, 1800) * env(n, .002, .16) * .8
def rhodes(notes, d):
    n = int(d * SR); t = np.arange(n) / SR; s = np.zeros(n)
    for m in notes:
        f = mtof(m); s += (np.sin(2 * np.pi * f * t) + .35 * np.sin(2 * np.pi * 2 * f * t) * np.exp(-t * 4)) * (1 + .15 * np.sin(2 * np.pi * 5 * t))
    return s / len(notes) * env(n, .006, .9) * .5
def brass(notes, d=.28):
    n = int(d * SR); t = np.arange(n) / SR; s = np.zeros(n)
    for m in notes:
        for dt in (0, .08, -.07): s += 2 * ((t * mtof(m) * 2 ** (dt / 12)) % 1) - 1
    return lp(s / (3 * len(notes)), 3200) * env(n, .012, .2) * .55
def riser(d):
    n = int(d * SR); tt = np.arange(n) / n; nz = rng.standard_normal(n); out = np.zeros(n)
    for i in range(0, n, 1024): out[i:i + 1024] = hp(nz[i:i + 1024], 200 + 6000 * tt[i] ** 2)[:len(out[i:i + 1024])]
    return out * tt ** 2 * .35
def impact():
    n = int(1.4 * SR); t = np.arange(n) / SR
    return np.tanh((np.sin(2 * np.pi * np.cumsum(40 + 80 * np.exp(-t * 14)) / SR) * np.exp(-t * 3) + lp(rng.standard_normal(n), 2500) * np.exp(-t * 6) * .5) * 1.6)
K, S, C = kick(), snare(), clap()
# progressione Dm9 - G13 - Cmaj9 - A7sus (funk in Re minore)
CH = [[62, 65, 69, 72, 76], [59, 64, 65, 69, 71], [60, 64, 67, 71, 74], [57, 62, 64, 67, 71]]
BS = [38, 43, 36, 45]
END_ST = TL['segs'][-1][1]
t = 0.; beat = 0
while t < TOTAL + .3:
    bar = beat // 4; pos = beat % 4; ch = bar % 4
    pre = BOOM - 2 * B < t < BOOM  # break prima del BOOM
    intro = t < TL['segs'][1][1]
    vol = .55 if (not intro and t < END_ST) else .8   # sotto la voce
    if not pre:
        add(K, t, .9 * vol)
        if pos in (1, 3): add(S, t, .55 * vol); add(C, t, .5 * vol, .1)
        if pos == 2 and beat % 8 == 6: add(K, t + B / 2, .6 * vol)
        for k in range(4): add(shaker(), t + k * B / 4, (.8 if k % 2 else .45) * vol, -.3)
        # basso slap sincopato
        for o, dm in [(0, 0), (.75, 12), (1.5, 0), (2.5, 7), (3.25, 10)]:
            if pos == int(o) and not intro: add(slap(BS[ch] + dm), t + (o - int(o)) * B, .7 * vol)
        if pos == 0: add(rhodes(CH[ch], 4 * B), t, .45 * vol, .2)
    t += B; beat += 1
# hook iniziale: stab di fiati sulla "SFIDA"
for k, st in enumerate([0.15, .15 + 2 * B / 4, .15 + 3 * B / 4, .15 + 4 * B / 4]):
    add(brass([62, 65, 69] if k < 3 else [64, 67, 71]), st, .7)
add(riser(2 * B), BOOM - 2 * B, .7)
add(impact(), BOOM, 1.0); add(brass([62, 65, 69, 74], .5), BOOM, .8)
# stab sul totale finale e sull'end card
seg8 = [s for s in TL['segs'] if s[0] == 'L2'][0]
add(brass([65, 69, 72, 76], .4), seg8[1] + .6, .7); add(impact(), seg8[1] + .6, .5)
add(brass([62, 65, 69, 74], .6), END_ST, .7)
# chiusura
fade = np.ones(N); fe = int((TOTAL + .3) * SR); fs = int((TOTAL - .8) * SR)
fade[fs:fe] = np.linspace(1, 0, fe - fs); fade[fe:] = 0
L *= fade; R *= fade
st = np.stack([L, R], 1); st = st / np.max(np.abs(st)) * .9
wavfile.write(f'{HERE}/mus_{LG}.wav', SR, (st * 32767).astype(np.int16)); print('ok')

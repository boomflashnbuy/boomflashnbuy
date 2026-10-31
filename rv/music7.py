"""Original upbeat commercial track (synthesised, royalty-free) for the Say'n'Buy story."""
import numpy as np
from scipy.signal import butter, sosfilt
from scipy.io import wavfile

SR = 44100
DUR = 34.0
N = int(SR * DUR)
BPM = 118
B = 60 / BPM            # beat length
OFF = 3.5 - 7 * B        # so that a downbeat (bar start) lands exactly on 2.6 s (the drop)
DROP = 3.5
OUTRO = 28.5
CUTS = [9.0, 12.5, 16.0, 20.0, 23.5]

L = np.zeros(N); R = np.zeros(N)
t_all = np.arange(N) / SR

def add(sig, start, gain=1.0, pan=0.0):
    i = int(start * SR)
    if i >= N: return
    j = min(N, i + len(sig)); s = sig[: j - i] * gain
    L[i:j] += s * (1 - pan) ; R[i:j] += s * (1 + pan)

def env(n, a=0.005, d=0.2):
    t = np.arange(n) / SR
    e = np.minimum(1, t / a) * np.exp(-t / d)
    return e

def lp(x, f):
    return sosfilt(butter(2, f, 'low', fs=SR, output='sos'), x)

def hp(x, f):
    return sosfilt(butter(2, f, 'high', fs=SR, output='sos'), x)

rng = np.random.default_rng(7)

# --- drums
def kick():
    n = int(.42 * SR); t = np.arange(n) / SR
    f = 48 + 110 * np.exp(-t * 32)
    ph = 2 * np.pi * np.cumsum(f) / SR
    s = np.sin(ph) * np.exp(-t * 7.5)
    s += 0.25 * np.exp(-t * 300) * rng.standard_normal(n)  # click
    return np.tanh(s * 1.6)

def clap():
    n = int(.3 * SR); nz = hp(rng.standard_normal(n), 900)
    e = np.zeros(n)
    for k, o in enumerate([0, .011, .022]):
        i = int(o * SR)
        e[i:] += env(n - i, .001, .012 if k < 2 else .12)
    return lp(nz, 6000) * e * .6

def hat(open_=False):
    n = int((.25 if open_ else .06) * SR)
    return hp(rng.standard_normal(n), 7000) * env(n, .001, .09 if open_ else .018) * .35

K, CL, HC, HO = kick(), clap(), hat(), hat(True)

# beat positions
beats = []
t = OFF
while t < DUR: beats.append(t); t += B

side = np.ones(N)  # sidechain envelope
for bt in beats:
    if bt < 0: continue
    bi = round((bt - OFF) / B)
    in_drop = DROP - 0.01 <= bt < OUTRO + 4 * B
    in_intro = bt < DROP
    in_outro = bt >= OUTRO + 4 * B
    if in_drop or in_outro:
        add(K, bt, .95)
        i = int(bt * SR); m = min(N, i + int(.3 * SR))
        side[i:m] = np.minimum(side[i:m], 1 - .65 * np.exp(-np.arange(m - i) / SR / .09))
        if bi % 2 == 1: add(CL, bt, .7)
        add(HC, bt + B / 2, .55, .3)
        if bi % 4 == 3: add(HO, bt + B / 2, .35, -.3)
        add(HC, bt + B / 4, .25, -.4); add(HC, bt + 3 * B / 4, .25, .4)
    elif in_intro and bt > 0.4:
        add(HC, bt, .35, .2)  # ticking intro

# snare/clap roll before drop
for k in range(8):
    add(CL, DROP - 1.0 + k * (1.0 / 8), .18 + .06 * k)

# --- harmony: Am F C G (A minor, uplifting pop-house)
PROG = [[57, 60, 64, 69], [53, 57, 60, 65], [48, 52, 55, 60], [55, 59, 62, 67]]
BASS = [45, 41, 48, 43]
mtof = lambda m: 440 * 2 ** ((m - 69) / 12)
BAR = 4 * B

def saw(f, n, det=(0, -.11, .09, -.05, .06)):
    t = np.arange(n) / SR; s = np.zeros(n)
    for d in det:
        ff = f * 2 ** (d / 12)
        ph = (t * ff + rng.random()) % 1
        s += 2 * ph - 1
    return s / len(det)

def chord_stab(notes, n, cutoff):
    s = sum(saw(mtof(m), n) for m in notes) / len(notes)
    s = lp(s, cutoff)
    return s * env(n, .004, .16)

def pad(notes, n, cutoff):
    s = sum(saw(mtof(m), n) for m in notes) / len(notes)
    a = np.minimum(1, np.arange(n) / SR / .4)
    return lp(s, cutoff) * a

bar_starts = []
t = DROP - 4 * BAR * 0  # bars aligned to drop
t = OFF
while t < DUR: bar_starts.append(t); t += BAR

for bs in bar_starts:
    if bs + BAR < 0: continue
    bi = round((bs - OFF) / BAR)
    ch, bn = PROG[bi % 4], BASS[bi % 4]
    if bs < DROP - 0.01:
        # intro: filtered pad rising
        n = int(BAR * SR); p = pad(ch, n, 400 + 900 * max(0, bs + BAR) / DROP)
        add(p, max(0, bs), .22)
        continue
    # off-beat chord stabs (house)
    for k in range(8):
        st = bs + k * B / 2
        if k % 2 == 1:
            add(chord_stab([m + 12 for m in ch], int(.22 * SR), 3200), st, .34, (-.25 if k % 4 == 1 else .25))
    # bass: 8th notes, octave jumps
    for k in range(8):
        st = bs + k * B / 2; f = mtof(bn - 12 + (12 if k % 2 else 0))
        n = int(B / 2 * .9 * SR)
        s = lp(saw(f, n, (0, .04)), 900) * env(n, .003, .18)
        add(np.tanh(s * 1.8), st, .5)
    # soft pad underneath
    add(pad(ch, int(BAR * SR), 1400), bs, .10)

# --- lead hook (pluck arp), in drop only, every other bar
ARP = [[69, 72, 76, 72], [65, 69, 72, 69], [64, 67, 72, 67], [67, 71, 74, 71]]
for bs in bar_starts:
    if bs < DROP - 0.01 or bs > OUTRO + 2 * BAR: continue
    bi = round((bs - OFF) / BAR)
    a = ARP[bi % 4]
    for k in range(16):
        st = bs + k * B / 4
        m = a[k % 4] + (12 if k in (6, 14) else 0)
        n = int(.18 * SR); tt = np.arange(n) / SR
        s = (np.sin(2 * np.pi * mtof(m) * tt) + .4 * np.sin(4 * np.pi * mtof(m) * tt)) * env(n, .002, .07)
        add(s, st, .16, .35 * np.sin(k))

# --- transitions: whoosh + impact on each cut
def whoosh(d=.7):
    n = int(d * SR); nz = rng.standard_normal(n)
    tt = np.arange(n) / n
    out = np.zeros(n); seg = 512
    for i in range(0, n, seg):
        fc = 300 + 7000 * tt[i] ** 2
        out[i:i + seg] = lp(nz[i:i + seg + 0], min(fc, 18000))[: len(out[i:i + seg])]
    return out * np.sin(np.pi * tt) ** 2 * .5

def impact():
    n = int(1.2 * SR); t = np.arange(n) / SR
    s = np.sin(2 * np.pi * (40 + 60 * np.exp(-t * 18)) * t) * np.exp(-t * 3.2)
    s += lp(rng.standard_normal(n), 2500) * np.exp(-t * 6) * .4
    return np.tanh(s * 1.4)

W = whoosh()
for c in CUTS:
    add(W, c - .6, .5, (-.3 if CUTS.index(c) % 2 else .3))
add(impact(), DROP, .55); add(impact(), OUTRO, .65)

# riser into drop
n = int(2.2 * SR); tt = np.arange(n) / SR
rise = np.sin(2 * np.pi * np.cumsum(200 + 900 * (tt / 2.2) ** 2) / SR) * (tt / 2.2) ** 2 * .12
add(rise + whoosh(2.2)[:n] * .5, DROP - 2.2, .8)


# --- SFX: pops on bubbles, clicks on taps, booms on key moments
def pop():
    n=int(.16*SR);t=np.arange(n)/SR
    f=900+1400*np.exp(-t*40)
    return np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t*28)*.6
def click():
    n=int(.05*SR);return hp(rng.standard_normal(n),2500)*env(n,.0005,.008)*.9
def beep():
    n=int(.22*SR);t=np.arange(n)/SR;return (np.sin(2*np.pi*1760*t)+.5*np.sin(2*np.pi*2640*t))*np.minimum(1,t/.005)*np.exp(-t*9)*.35
from scipy.io import wavfile as _wf
def _ld(p):
    sr,x=_wf.read(p);x=x.astype(float)/32768
    return x
BEEP=_ld('../snd/beep.wav');KC=_ld('../snd/kaching.wav')
add(BEEP,11.48,.9);add(KC,17.85,.8)
for tt in [11.6,12.9,20.6]: add(pop(),tt,.4)
for tt in [17.85]: add(click(),tt,.8)
add(impact(),11.48,.5)
# --- mix
L *= side; R *= side
mix = np.stack([L, R], 1)
mix = hp(mix.T, 30).T
# fade in/out
fi = int(.08 * SR); fo = int(1.6 * SR)
mix[:fi] *= np.linspace(0, 1, fi)[:, None]
mix[-fo:] *= np.linspace(1, 0, fo)[:, None] ** 1.5
mix = np.tanh(mix * 1.25)
mix /= np.max(np.abs(mix)) / .89
wavfile.write('music5.wav', SR, (mix * 32767).astype(np.int16))
print('ok', mix.shape[0] / SR)

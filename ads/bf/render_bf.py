"""Spot Black Friday Giulia + Luca — render 1080x1920 30fps da scene B1-B4, schermata offerte, voci Cleo/Enzo.
uso: python3 render_bf.py it            -> BFB-BlackFriday-it.mp4 (video + musica + voci, -14 LUFS)
     python3 render_bf.py it 1.0,9.5    -> solo fotogrammi di prova f_<t>.jpg
Struttura: aggancio 2,6 s solo immagine+musica ("SCONTO VERO?"), poi Giulia, Luca, BOOM, offerte con -50 €, chiusura e scheda finale.
"""
import json, sys, math, subprocess, os
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import soundfile as sf
from scipy.signal import resample_poly

LG = sys.argv[1]
D = os.path.dirname(os.path.abspath(__file__))
W, H, FPS = 1080, 1920, 30
LIME = (212, 255, 74); INK = (11, 12, 10); RED = (255, 80, 80)
F = lambda n, s: ImageFont.truetype(f'{D}/ttf/{n}.ttf', s)
EXO = lambda s: F('exo900i', s); SORA = lambda s: F('sora800', s); SORA7 = lambda s: F('sora700', s)

EUR = (lambda v: f'€{v}') if LG == 'en' else (lambda v: f'{v} €')
TX = {
 'it': dict(hook='SCONTO VERO?', store='IN NEGOZIO', tag='SCANSIONA PRIMA DI PAGARE', end1='Gratis, dal browser', end2='Link nel profilo',
            disc='Prezzi a titolo di esempio. I prezzi su Amazon variano.',
            sub=['Black Friday: friggitrice ad aria, da *249 €* a *179 €*. Affare?', 'Prima di pagare, *inquadra il codice*.', '',
                 'Su Amazon *129 €*. Altro che sconto: altri *50 €* in meno!', 'Black Friday: *scansiona prima di pagare*. *BoomFlashnBuy*, gratis dal browser.']),
 'en': dict(hook='REAL DEAL?', store='IN STORE', tag='SCAN BEFORE YOU PAY', end1='Free, in your browser', end2='Link in bio',
            disc='Example prices. Amazon prices vary.',
            sub=['Black Friday: air fryer, down from *€249* to *€179*. A bargain?', 'Before you pay, *scan the barcode*.', '',
                 'On Amazon *€129*. Some discount: *€50* less!', 'Black Friday: *scan before you pay*. *BoomFlashnBuy*, free in your browser.']),
 'es': dict(hook='¿DESCUENTO REAL?', store='EN TIENDA', tag='ESCANEA ANTES DE PAGAR', end1='Gratis, desde el navegador', end2='Enlace en la bio',
            disc='Precios de ejemplo. Los precios en Amazon varían.',
            sub=['Black Friday: freidora de aire, de *249 €* a *179 €*. ¿Una ganga?', 'Antes de pagar, *escanea el código*.', '',
                 'En Amazon *129 €*. ¡Menudo descuento: *50 €* menos!', 'Black Friday: *escanea antes de pagar*. *BoomFlashnBuy*, gratis desde el navegador.']),
}[LG]

# voci: ordine di battuta
VO = ['G1', 'L1', 'BOOM', 'G2', 'L2']
VOD = f'{D}/vo_{LG}'
vlen = [sf.info(f'{VOD}/{n}.wav').duration for n in VO]

def cover(im, k=1.0):
    r = max(W / im.width, H / im.height) * k
    return im.resize((int(im.width * r), int(im.height * r)), Image.LANCZOS)
IM = {k: cover(Image.open(f'{D}/{k}.jpg').convert('RGB'), 1.25) for k in ['B1', 'B2', 'B3', 'B4']}
OFF = Image.open(f'{D}/app/off_{LG}.png').convert('RGB')
LOGO = Image.open(f'{D}/logo.png').convert('RGBA')

ease = lambda x: 1 - (1 - min(max(x, 0), 1)) ** 3
def kb(key, u, z0=1.1, z1=1.18, fx=.5, fy=.42, fx1=None, fy1=None):
    """Ken Burns (zoom minimo 1.1 per tagliare il segno nell'angolo in basso a destra)."""
    src = IM[key]; z = z0 + (z1 - z0) * u
    base = min(src.width / W, src.height / H); cw, ch = W * base / z, H * base / z
    fx1 = fx if fx1 is None else fx1; fy1 = fy if fy1 is None else fy1
    cx = (fx + (fx1 - fx) * u) * src.width; cy = (fy + (fy1 - fy) * u) * src.height
    x0 = min(max(cx - cw / 2, 0), src.width - cw); y0 = min(max(cy - ch / 2, 0), src.height - ch)
    return src.crop((int(x0), int(y0), int(x0 + cw), int(y0 + ch))).resize((W, H), Image.BILINEAR)

def rr(d, box, r, **kw): d.rounded_rectangle(box, r, **kw)
def text_w(f, s): b = f.getbbox(s); return b[2] - b[0]

def caption(fr, s, a=1.0, y=1470):
    """sottotitolo: parole tra * * in lime."""
    if a <= 0 or not s: return
    f = SORA(54); words = s.split(' '); rows = []; cur = []
    for w_ in words:
        test = ' '.join(x.replace('*', '') for x in cur + [w_])
        if text_w(f, test) > 900 and cur: rows.append(cur); cur = [w_]
        else: cur.append(w_)
    rows.append(cur)
    lh = 72; bh = lh * len(rows) + 44
    ov = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    rr(d, (60, y, W - 60, y + bh), 34, fill=INK + (int(205 * a),))
    yy = y + 22; hl = False
    for row in rows:
        tw = text_w(f, ' '.join(x.replace('*', '') for x in row)); xx = (W - tw) / 2
        for w_ in row:
            st = w_.startswith('*'); en = w_.rstrip('.,!?:;').endswith('*')
            on = hl or st; t = w_.replace('*', '')
            d.text((xx, yy), t, font=f, fill=(LIME if on else (255, 255, 255)) + (int(255 * a),))
            xx += text_w(f, t + ' ')
            hl = (hl or st) and not en
        yy += lh
    fr.alpha_composite(ov)

def price_tag(fr, u, y=330):
    """etichetta negozio: 249 barrato -> 179 (entra con un pop)."""
    if u <= 0: return
    s = 0.6 + 0.4 * ease(u * 2.2) + 0.06 * math.sin(min(u * 2.2, 1) * math.pi)
    f1 = SORA(40); f2 = EXO(150); f3 = SORA(58)
    top, old, new = TX['store'], EUR(249), EUR(179)
    w = max(text_w(f1, top), text_w(f2, new) + text_w(f3, old) + 50) + 120; h = 290
    ov = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    rr(d, (0, 0, w, h), 46, fill=INK + (225,), outline=LIME + (255,), width=6)
    d.text(((w - text_w(f1, top)) / 2, 30), top, font=f1, fill=(205, 212, 198))
    x0 = (w - (text_w(f3, old) + 50 + text_w(f2, new))) / 2
    d.text((x0, 125), old, font=f3, fill=(170, 176, 165)); ow = text_w(f3, old)
    d.line((x0 - 6, 168, x0 + ow + 6, 150), fill=RED + (255,), width=9)
    d.text((x0 + ow + 50, 78), new, font=f2, fill=(255, 255, 255))
    ov = ov.resize((max(1, int(w * s)), max(1, int(h * s))), Image.LANCZOS)
    fr.alpha_composite(ov, (int(W / 2 - ov.width / 2), int(y - ov.height / 2)))

def phone(fr, scr, u, y_end=170, w=640):
    """telefono con la schermata dell'app che sale dal basso."""
    if u <= 0: return
    e = ease(u * 1.6); h = int(w * scr.height / scr.width)
    sc = scr.resize((w, h), Image.LANCZOS).convert('RGBA')
    m = Image.new('L', (w, h), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, w, h), 54, fill=255); sc.putalpha(m)
    fw, fh = w + 36, h + 36
    body = Image.new('RGBA', (fw, fh + 40), (0, 0, 0, 0)); d = ImageDraw.Draw(body)
    rr(d, (0, 0, fw, fh), 70, fill=(20, 22, 18, 255), outline=(70, 76, 64, 255), width=4)
    body.alpha_composite(sc, (18, 18))
    y = int(H + 40 - (H + 40 - y_end) * e)
    glow = Image.new('RGBA', (fw + 120, fh + 120), (0, 0, 0, 0)); ImageDraw.Draw(glow).rounded_rectangle((60, 60, fw + 60, fh + 60), 80, fill=LIME + (90,))
    glow = glow.filter(ImageFilter.GaussianBlur(40))
    fr.alpha_composite(glow, ((W - fw) // 2 - 60, y - 60)); fr.alpha_composite(body, ((W - fw) // 2, y))

def badge(fr, s, u, x=W // 2, y=1250, sz=170):
    if u <= 0: return
    k = 0.3 + 0.7 * ease(u * 3) + 0.12 * math.sin(min(u * 3, 1) * math.pi)
    f = EXO(sz); tw = text_w(f, s); bw, bh = tw + 110, sz + 90
    ov = Image.new('RGBA', (bw, bh), (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    rr(d, (0, 0, bw, bh), bh // 2, fill=LIME + (255,)); d.text((55, 22), s, font=f, fill=INK)
    ov = ov.rotate(-4, expand=True, resample=Image.BICUBIC)
    ov = ov.resize((max(1, int(ov.width * k)), max(1, int(ov.height * k))), Image.LANCZOS)
    fr.alpha_composite(ov, (int(x - ov.width / 2), int(y - ov.height / 2)))

def big_text(fr, s, u, y, sz=170, col=LIME):
    if u <= 0: return
    f = EXO(sz)
    while text_w(f, s) > W - 90: sz -= 8; f = EXO(sz)
    k = .6 + .4 * ease(u * 3); tw = text_w(f, s)
    ov = Image.new('RGBA', (tw + 80, sz + 110), (0, 0, 0, 0)); ImageDraw.Draw(ov).text((40, 20), s, font=f, fill=col, stroke_width=12, stroke_fill=INK)
    ov = ov.resize((int(ov.width * k), int(ov.height * k)), Image.LANCZOS)
    fr.alpha_composite(ov, ((W - ov.width) // 2, int(y - ov.height / 2)))

def boom(fr, u):
    if u <= 0 or u >= 1: return
    fl = Image.new('RGBA', (W, H), (255, 255, 255, int(255 * max(0, 1 - u * 3.5)))); fr.alpha_composite(fl)
    k = 0.5 + 0.7 * ease(u * 2.5); sh = int(18 * math.sin(u * 60) * (1 - u))
    f = EXO(250); s = 'BOOM!'; tw = text_w(f, s)
    ov = Image.new('RGBA', (tw + 80, 340), (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    d.text((40, 20), s, font=f, fill=LIME, stroke_width=10, stroke_fill=INK)
    ov = ov.resize((int(ov.width * k), int(ov.height * k)), Image.LANCZOS)
    a = 1 if u < .8 else (1 - u) / .2
    ov.putalpha(ov.getchannel('A').point(lambda v: int(v * a)))
    fr.alpha_composite(ov, (int(W / 2 - ov.width / 2) + sh, int(800 - ov.height / 2)))

def disclaimer(fr):
    f = SORA7(30); s = TX['disc']; tw = text_w(f, s)
    ImageDraw.Draw(fr).text(((W - tw) / 2, H - 92), s, font=f, fill=(235, 238, 230, 210), stroke_width=3, stroke_fill=(0, 0, 0, 180))

def dim(fr, a): fr.alpha_composite(Image.new('RGBA', (W, H), (0, 0, 0, int(255 * a))))

# ---------- timeline ----------
PAD = .3; HOOK = 2.6
T = [('hook', 0.0, HOOK, None)]; t = HOOK
for i, n in enumerate(VO):
    dur = vlen[i] + 0.55 if n == 'BOOM' else vlen[i] + PAD * 2 + (1.2 if n == 'G2' else 0) + (0.5 if n == 'L2' else 0)
    T.append((n, t, dur, i)); t += dur
T.append(('end', t, 3.2, None)); t += 3.2
TOTAL = t
VOAT = [[s[1] + (0.05 if s[0] == 'BOOM' else PAD) + (1.0 if s[0] == 'G2' else 0), s[0]] for s in T if s[3] is not None]
json.dump({'segs': T, 'vo': VOAT, 'total': TOTAL, 'boom': [s[1] for s in T if s[0] == 'BOOM'][0]}, open(f'{D}/timeline_{LG}.json', 'w'))

def frame(tt):
    for name, st, du, vi in T:
        if st <= tt < st + du: break
    u = (tt - st) / du; lt = tt - st
    if name == 'hook':
        fr = kb('B1', u * .4, 1.12, 1.22, .5, .40).convert('RGBA')
        big_text(fr, TX['hook'], (lt - .25) / .9, 470)
        price_tag(fr, (lt - .9) / 1.0, y=1250)
        return fr
    if name == 'end':
        fr = Image.new('RGBA', (W, H), INK + (255,))
        k = .7 + .3 * ease(u * 4); lg_ = LOGO.resize((int(560 * k), int(560 * k)), Image.LANCZOS)
        fr.alpha_composite(lg_, ((W - lg_.width) // 2, 420 + (560 - lg_.height) // 2))
        d = ImageDraw.Draw(fr)
        for s, f, c, y in [(TX['end1'], EXO(92), LIME, 1060), ('boomflashnbuy.netlify.app', SORA(56), (255, 255, 255), 1210), (TX['end2'], SORA(52), LIME, 1330)]:
            d.text(((W - text_w(f, s)) / 2, y), s, font=f, fill=c)
        f = SORA7(30); s = TX['disc']; d.text(((W - text_w(f, s)) / 2, H - 120), s, font=f, fill=(150, 156, 146))
        return fr
    if name == 'G1':
        fr = kb('B1', .4 + u * .6, 1.12, 1.22, .5, .40).convert('RGBA'); price_tag(fr, 1, y=330)
    elif name == 'L1':
        fr = kb('B2', u, 1.1, 1.2, .55, .40, .6, .45).convert('RGBA')
    elif name == 'BOOM':
        fr = kb('B3', u, 1.12, 1.25, .5, .42).convert('RGBA'); boom(fr, u)
    elif name == 'G2':
        fr = kb('B3', 1, 1.25, 1.28, .5, .42).filter(ImageFilter.GaussianBlur(14)).convert('RGBA'); dim(fr, .35)
        phone(fr, OFF, lt / 1.1, y_end=170); badge(fr, ('−' if LG != 'en' else '−') + EUR(50), (lt - 1.4) / 1.0, y=1300); disclaimer(fr)
    else:  # L2
        fr = kb('B4', u, 1.1, 1.2, .5, .38).convert('RGBA')
        a = ease((lt - .4) * 2)
        if a > 0: dim(fr, .25 * a); big_text(fr, TX['tag'], (lt - .4) / .9, 420, sz=118, col=LIME)
    if name != 'BOOM':
        a = min(1, lt * 6, (du - lt) * 6)
        caption(fr, TX['sub'][vi], a, y=1470 if name != 'G2' else 1560)
    return fr

def audio(out_wav):
    """voci posizionate + musica sotto la voce (ducking), -14 LUFS."""
    subprocess.run(['python3', f'{D}/music_bf.py', LG], check=True)
    SR = 44100; mus, msr = sf.read(f'{D}/mus_{LG}.wav'); N = len(mus)
    voc = np.zeros(N)
    for st, n in VOAT:
        x, sr = sf.read(f'{VOD}/{n}.wav'); x = x if x.ndim == 1 else x.mean(1)
        if sr != SR: x = resample_poly(x, SR, sr)
        i = int(st * SR); j = min(N, i + len(x)); voc[i:j] += x[:j - i] * (1.25 if n == 'BOOM' else 1.0)
    env = np.abs(voc); k = int(.25 * SR)
    env = np.convolve(env > 0.01, np.ones(k) / k, mode='same')
    duck = 1 - 0.55 * np.clip(env * 3, 0, 1)
    mix = mus * duck[:, None] * 0.75 + voc[:, None] * 0.95
    mix /= max(1e-6, np.abs(mix).max()) / 0.95
    sf.write(f'{D}/mix_raw_{LG}.wav', mix, SR)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', f'{D}/mix_raw_{LG}.wav', '-af', 'loudnorm=I=-14:TP=-1.5:LRA=11', '-ar', '48000', out_wav], check=True)

if __name__ == '__main__':
    only = sys.argv[2] if len(sys.argv) > 2 else None
    if only:
        for s in only.split(','): frame(float(s)).convert('RGB').save(f'{D}/f_{s}.jpg', quality=88)
        sys.exit()
    vid = f'{D}/v_{LG}.mp4'
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-preset', 'medium', '-crf', '19', '-pix_fmt', 'yuv420p', vid], stdin=subprocess.PIPE)
    for k in range(int(TOTAL * FPS)): p.stdin.write(frame(k / FPS).convert('RGB').tobytes())
    p.stdin.close(); p.wait()
    audio(f'{D}/a_{LG}.wav')
    out = f'{D}/BFB-BlackFriday-{LG}.mp4'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', vid, '-i', f'{D}/a_{LG}.wav', '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-shortest', out], check=True)
    print('ok', round(TOTAL, 2), out)

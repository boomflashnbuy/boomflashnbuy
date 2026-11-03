"""Spot Giulia + Luca "La sfida" — render 1080x1920 30fps da immagini + schermate app + voci.
uso: python3 render_duo.py it   -> out_it.mp4 (solo video) + timeline_it.json
"""
import json, sys, math, subprocess, os
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import soundfile as sf

LG = sys.argv[1]
D = os.path.dirname(os.path.abspath(__file__))
W, H, FPS = 1080, 1920, 30
LIME = (212, 255, 74); INK = (11, 12, 10)
F = lambda n, s: ImageFont.truetype(f'{D}/ttf/{n}.ttf', s)
EXO = lambda s: F('exo900i', s); SORA = lambda s: F('sora800', s); SORA7 = lambda s: F('sora700', s)

lines = json.load(open(f'{D}/lines.json'))
TX = json.load(open(f'{D}/tx.json'))[LG]
VOD = f'{D}/vo_{LG}'
vlen = [sf.info(f'{VOD}/{i}.wav').duration for i in range(1, len(lines[LG]) + 1)]

def img(p):
    return Image.open(p).convert('RGB')
def cover(im, w=W, h=H, k=1.18):
    r = max(w / im.width, h / im.height) * k
    return im.resize((int(im.width * r), int(im.height * r)), Image.LANCZOS)
IM = {k: cover(img(f'{D}/{k}.jpg')) for k in ['QA', 'PB', 'QC', 'PD', 'SE', 'SF', 'F6']}
APP = {k: img(f'{D}/app/{LG}/{k}.png') for k in ['off_bag', 'off_sc', 'card_bag', 'card_sc']}
LOGO = Image.open(f'{D}/../logo.png').convert('RGBA')

ease = lambda x: 1 - (1 - min(max(x, 0), 1)) ** 3
def kb(key, u, z0=1.0, z1=1.08, fx=.5, fy=.45, fx1=None, fy1=None):
    """Ken Burns: u in [0,1]."""
    src = IM[key]; z = z0 + (z1 - z0) * u
    cw, ch = W / z * (src.width / (W * 1.18)) * 1.18 / (src.width / W) , 0
    # crop window in source pixels
    s = src.width / (W * 1.18) * 1.18  # source px per output px at z=1 (cover)
    base = min(src.width / W, src.height / H)
    cw, ch = W * base / z, H * base / z
    fx1 = fx if fx1 is None else fx1; fy1 = fy if fy1 is None else fy1
    cx = (fx + (fx1 - fx) * u) * src.width; cy = (fy + (fy1 - fy) * u) * src.height
    x0 = min(max(cx - cw / 2, 0), src.width - cw); y0 = min(max(cy - ch / 2, 0), src.height - ch)
    return src.crop((int(x0), int(y0), int(x0 + cw), int(y0 + ch))).resize((W, H), Image.BILINEAR)

def rr(d, box, r, **kw): d.rounded_rectangle(box, r, **kw)

def text_w(f, s): return f.getbbox(s)[2] - f.getbbox(s)[0]

def caption(fr, s, a=1.0, y=1470):
    """sottotitolo: parole tra * * in lime."""
    if a <= 0: return
    f = SORA(54); words = s.split(' '); rows = []; cur = []
    for w_ in words:
        test = ' '.join(x.replace('*', '') for x in cur + [w_])
        if text_w(f, test) > 900 and cur: rows.append(cur); cur = [w_]
        else: cur.append(w_)
    rows.append(cur)
    lh = 72; bh = lh * len(rows) + 44
    ov = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    rr(d, (60, y, W - 60, y + bh), 34, fill=(11, 12, 10, int(205 * a)))
    yy = y + 22
    for row in rows:
        tw = text_w(f, ' '.join(x.replace('*', '') for x in row)); xx = (W - tw) / 2
        for w_ in row:
            hl = w_.startswith('*'); t = w_.replace('*', '')
            d.text((xx, yy), t, font=f, fill=(LIME if hl else (255, 255, 255)) + (int(255 * a),))
            xx += text_w(f, t + ' ')
        yy += lh
    fr.alpha_composite(ov)

def chip(fr, top, big, u, x=W // 2, y=300, col=(255, 255, 255), strike=False):
    """etichetta prezzo che entra con un pop."""
    if u <= 0: return
    s = 0.6 + 0.4 * ease(u * 2.2) + 0.06 * math.sin(min(u * 2.2, 1) * math.pi)
    f1 = SORA(40); f2 = EXO(150)
    w1, w2 = text_w(f1, top), text_w(f2, big); bw = max(w1, w2) + 120; bh = 290
    ov = Image.new('RGBA', (bw, bh), (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    rr(d, (0, 0, bw, bh), 46, fill=(11, 12, 10, 225), outline=LIME + (255,), width=6)
    d.text(((bw - w1) / 2, 30), top, font=f1, fill=(205, 212, 198))
    d.text(((bw - w2) / 2, 78), big, font=f2, fill=col)
    if strike:
        d.line((60, 170, bw - 60, 150), fill=(255, 80, 80), width=12)
    ov = ov.resize((max(1, int(bw * s)), max(1, int(bh * s))), Image.LANCZOS)
    fr.alpha_composite(ov, (int(x - ov.width / 2), int(y - ov.height / 2)))

def phone(fr, scr, u, y_end=250, w=640, label=None):
    """telefono con schermata app che sale dal basso."""
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
    if label and u > .35:
        a = min(1, (u - .35) * 4); f = SORA(44); tw = text_w(f, label)
        ov = Image.new('RGBA', (tw + 70, 92), (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
        rr(d, (0, 0, tw + 70, 92), 46, fill=LIME + (int(255 * a),)); d.text((35, 18), label, font=f, fill=INK + (int(255 * a),))
        fr.alpha_composite(ov, ((W - ov.width) // 2, y - 120))

def badge(fr, s, u, x=W // 2, y=1250, sz=170):
    if u <= 0: return
    k = 0.3 + 0.7 * ease(u * 3) + 0.12 * math.sin(min(u * 3, 1) * math.pi)
    f = EXO(sz); tw = text_w(f, s); bw, bh = tw + 110, sz + 90
    ov = Image.new('RGBA', (bw, bh), (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    rr(d, (0, 0, bw, bh), bh // 2, fill=LIME + (255,)); d.text((55, 22), s, font=f, fill=INK)
    ov = ov.rotate(-4, expand=True, resample=Image.BICUBIC)
    ov = ov.resize((max(1, int(ov.width * k)), max(1, int(ov.height * k))), Image.LANCZOS)
    fr.alpha_composite(ov, (int(x - ov.width / 2), int(y - ov.height / 2)))

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
    d = ImageDraw.Draw(fr); d.text(((W - tw) / 2, H - 92), s, font=f, fill=(235, 238, 230, 210), stroke_width=3, stroke_fill=(0, 0, 0, 180))

def dim(fr, a):
    fr.alpha_composite(Image.new('RGBA', (W, H), (0, 0, 0, int(255 * a))))

def split(u, top='QA', bot='PB'):
    fr = Image.new('RGBA', (W, H), INK + (255,))
    a = kb(top, u, 1.25, 1.32, .5, .30).crop((0, H // 4 - 40, W, H // 4 - 40 + H // 2 - 6))
    b = kb(bot, u, 1.25, 1.32, .5, .30).crop((0, H // 4 - 40, W, H // 4 - 40 + H // 2 - 6))
    off = int((1 - ease(u * 3)) * W)
    fr.paste(a, (-off, 0)); fr.paste(b, (off, H // 2 + 6))
    d = ImageDraw.Draw(fr); d.rectangle((0, H // 2 - 6, W, H // 2 + 6), fill=LIME)
    return fr

# ---------- timeline ----------
PAD = .35
T = []  # (name, start, dur, vo_index or None)
t = 0.0
T.append(('hook', t, 2.4, None)); t += 2.4
for i, (shot, sp, _) in enumerate(lines[LG]):
    dur = vlen[i] + PAD * 2 + (0.4 if i in (5, 8) else 0)
    if i == 3: dur = vlen[i] + 0.5
    T.append((f'L{i}', t, dur, i)); t += dur
T.append(('end', t, 3.0, None)); t += 3.0
TOTAL = t
json.dump({'segs': T, 'vo': [[s[1] + (PAD if s[3] != 3 else 0.05), s[3] + 1] for s in T if s[3] is not None], 'total': TOTAL, 'boom': [s[1] for s in T if s[0] == 'L3'][0]},
          open(f'{D}/timeline_{LG}.json', 'w'))

SUB = TX['sub']
def frame(tt):
    for name, st, du, vi in T:
        if st <= tt < st + du: break
    u = (tt - st) / du; lt = tt - st
    if name == 'hook':
        fr = split(u)
        f = EXO(170); s = TX['hook']; tw = text_w(f, s); k = .6 + .4 * ease(u * 3)
        ov = Image.new('RGBA', (tw + 80, 240), (0, 0, 0, 0)); ImageDraw.Draw(ov).text((40, 20), s, font=f, fill=LIME, stroke_width=12, stroke_fill=INK)
        ov = ov.resize((int(ov.width * k), int(ov.height * k)), Image.LANCZOS)
        fr.alpha_composite(ov, ((W - ov.width) // 2, H // 2 - ov.height // 2))
        return fr
    if name == 'end':
        fr = Image.new('RGBA', (W, H), INK + (255,))
        lg_ = LOGO.resize((560, 560), Image.LANCZOS); k = .7 + .3 * ease(u * 4)
        lg_ = lg_.resize((int(560 * k), int(560 * k)), Image.LANCZOS)
        fr.alpha_composite(lg_, ((W - lg_.width) // 2, 420 + (560 - lg_.height) // 2))
        d = ImageDraw.Draw(fr)
        for s, f, c, y in [(TX['end1'], EXO(96), LIME, 1060), ('boomflashnbuy.netlify.app', SORA(56), (255, 255, 255), 1210), (TX['end2'], SORA(52), LIME, 1330)]:
            tw = text_w(f, s); d.text(((W - tw) / 2, y), s, font=f, fill=c)
        f = SORA7(30); s = TX['disc']; tw = text_w(f, s); d.text(((W - tw) / 2, H - 120), s, font=f, fill=(150, 156, 146))
        return fr
    i = vi; shot = lines[LG][i][0]
    if i == 0:
        fr = kb('QA', u, 1.0, 1.10, .5, .42).convert('RGBA'); chip(fr, TX['store'], '199 €', (lt - .5) / 1.2, y=330)
    elif i == 1:
        fr = kb('PB', u, 1.0, 1.10, .55, .45).convert('RGBA'); chip(fr, TX['store'], '299 €', (lt - .5) / 1.2, y=330)
    elif i == 2:
        fr = split(0.4 + u * .6)
        chip(fr, TX['bet'], '?', (lt - .2) / 1.0, y=H // 2, col=LIME)
    elif i == 3:
        fr = kb('QC', u, 1.08, 1.2, .55, .5).convert('RGBA'); boom(fr, u)
    elif i == 4:
        fr = kb('QC', .5 + u * .5, 1.2, 1.26, .55, .5).filter(ImageFilter.GaussianBlur(14)).convert('RGBA'); dim(fr, .35)
        phone(fr, APP['off_bag'], lt / 1.1, y_end=170); badge(fr, '−60 €', (lt - 1.3) / 1.0, y=1330); disclaimer(fr)
    elif i == 5:
        if lt < 1.2:
            fr = kb('PD', lt / 1.2, 1.0, 1.08, .5, .5).convert('RGBA')
        else:
            v = (lt - 1.2) / (du - 1.2)
            fr = kb('PD', 1, 1.08, 1.1, .5, .5).filter(ImageFilter.GaussianBlur(14)).convert('RGBA'); dim(fr, .35)
            phone(fr, APP['off_sc'], (lt - 1.2) / 1.1, y_end=170); badge(fr, '−50 €', (lt - 2.4) / 1.0, y=1330)
        disclaimer(fr)
    elif i == 6:
        fr = kb('SE', u, 1.0, 1.08, .5, .4).convert('RGBA')
        if lt > .5: dim(fr, .25 * min(1, (lt - .5) * 3))
        phone(fr, APP['card_bag'], (lt - .5) / 1.0, y_end=260, w=560, label=TX['sent'])
    elif i == 7:
        fr = kb('SF', u, 1.0, 1.08, .5, .4).convert('RGBA')
        if lt > .3: dim(fr, .25 * min(1, (lt - .3) * 3))
        phone(fr, APP['card_sc'], (lt - .3) / 1.0, y_end=260, w=560, label=TX['recv'])
    else:
        fr = kb('F6', u, 1.0, 1.12, .5, .38).convert('RGBA')
        f1 = EXO(110); f2 = EXO(230); a = ease((lt - .6) * 2)
        if a > 0:
            dim(fr, .3 * a); d = ImageDraw.Draw(fr)
            s1 = TX['tog']; s2 = '−110 €'
            d.text(((W - text_w(f1, s1)) / 2, 330), s1, font=f1, fill=(255, 255, 255, int(255 * a)), stroke_width=8, stroke_fill=INK)
            d.text(((W - text_w(f2, s2)) / 2, 460), s2, font=f2, fill=LIME + (int(255 * a),), stroke_width=12, stroke_fill=INK)
    if i != 3:
        a = min(1, lt * 6, (du - lt) * 6)
        caption(fr, SUB[i], a)
    return fr

if __name__ == '__main__':
    out = f'{D}/v_{LG}.mp4'
    p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
                          '-c:v', 'libx264', '-preset', 'medium', '-crf', '19', '-pix_fmt', 'yuv420p', out], stdin=subprocess.PIPE)
    n = int(TOTAL * FPS); only = sys.argv[2] if len(sys.argv) > 2 else None
    if only:
        for s in only.split(','):
            frame(float(s)).convert('RGB').save(f'{D}/f_{s}.jpg', quality=88)
        p.stdin.close(); p.wait(); sys.exit()
    for k in range(n):
        p.stdin.write(frame(k / FPS).convert('RGB').tobytes())
    p.stdin.close(); p.wait(); print('ok', TOTAL)

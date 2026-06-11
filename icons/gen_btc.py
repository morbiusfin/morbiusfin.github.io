"""Ícone MorbiusFin = moeda de Bitcoin dourada (combina com o splash)."""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math

S = 1024
img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
dr = ImageDraw.Draw(img)

# ---- fundo: radial verde escuro (igual ao splash) ----
bg = Image.new("RGBA", (S, S))
bgp = bg.load()
cx, cy = S * 0.5, S * 0.40
maxd = math.hypot(S, S) * 0.62
c_in, c_out = (14, 74, 54), (5, 17, 12)
for y in range(S):
    for x in range(S):
        t = min(1.0, math.hypot(x - cx, y - cy) / maxd)
        r = int(c_in[0] + (c_out[0] - c_in[0]) * t)
        g = int(c_in[1] + (c_out[1] - c_in[1]) * t)
        b = int(c_in[2] + (c_out[2] - c_in[2]) * t)
        bgp[x, y] = (r, g, b, 255)
img.alpha_composite(bg)

# ---- sombra da moeda ----
sh = Image.new("RGBA", (S, S), (0, 0, 0, 0))
shd = ImageDraw.Draw(sh)
shd.ellipse([S*0.22, S*0.74, S*0.78, S*0.88], fill=(0, 0, 0, 150))
sh = sh.filter(ImageFilter.GaussianBlur(28))
img.alpha_composite(sh)

# ---- disco dourado com gradiente radial (luz no canto superior-esquerdo) ----
R = int(S * 0.40)
ccx, ccy = S // 2, S // 2
coin = Image.new("RGBA", (S, S), (0, 0, 0, 0))
cp = coin.load()
# pontos de cor (do claro ao escuro)
stops = [(0.00, (255, 231, 163)), (0.30, (255, 206, 94)), (0.58, (245, 166, 35)),
         (0.80, (212, 134, 26)), (1.00, (169, 103, 15))]
def grad(t):
    for i in range(len(stops) - 1):
        t0, c0 = stops[i]; t1, c1 = stops[i + 1]
        if t <= t1:
            f = (t - t0) / (t1 - t0) if t1 > t0 else 0
            return tuple(int(c0[k] + (c1[k] - c0[k]) * f) for k in range(3))
    return stops[-1][1]
lx, ly = ccx - R * 0.32, ccy - R * 0.38   # foco da luz
for y in range(ccy - R - 2, ccy + R + 2):
    for x in range(ccx - R - 2, ccx + R + 2):
        d = math.hypot(x - ccx, y - ccy)
        if d <= R:
            t = min(1.0, math.hypot(x - lx, y - ly) / (R * 1.18))
            cp[x, y] = grad(t) + (255,)
coin = coin.filter(ImageFilter.GaussianBlur(0.6))
img.alpha_composite(coin)

# ---- aros (relevo): borda escura + anel de luz interno ----
dr.ellipse([ccx-R, ccy-R, ccx+R, ccy+R], outline=(150, 90, 12, 255), width=int(S*0.022))
ri = int(R * 0.86)
dr.ellipse([ccx-ri, ccy-ri, ccx+ri, ccy+ri], outline=(255, 240, 200, 120), width=int(S*0.012))
ro = int(R * 0.97)
dr.ellipse([ccx-ro, ccy-ro, ccx+ro, ccy+ro], outline=(120, 70, 8, 110), width=int(S*0.006))

# ---- símbolo ₿ (B bold + duas barras verticais) ----
sym = Image.new("RGBA", (S, S), (0, 0, 0, 0))
sd = ImageDraw.Draw(sym)
COL = (110, 68, 6, 255)
font = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", int(S*0.58))
bb = sd.textbbox((0, 0), "B", font=font)
bw, bh = bb[2] - bb[0], bb[3] - bb[1]
bx = ccx - bw / 2 - bb[0]
by = ccy - bh / 2 - bb[1]
sd.text((bx, by), "B", font=font, fill=COL)
# duas barrinhas verticais atravessando o B (em cima e embaixo)
barw = int(S * 0.030)
bar_top = ccy - bh / 2 - int(S*0.055)
bar_bot = ccy + bh / 2 + int(S*0.055)
gap = int(S * 0.052)
for offx in (-gap, 0):
    x0 = ccx - barw / 2 + offx - int(S*0.015)
    sd.rectangle([x0, bar_top, x0 + barw, bar_bot], fill=COL)
# leve realce branco em cima do símbolo (relevo)
hi = sym.copy()
hd = ImageDraw.Draw(hi)
img.alpha_composite(sym)

# brilho specular no topo da moeda
spec = Image.new("RGBA", (S, S), (0, 0, 0, 0))
spd = ImageDraw.Draw(spec)
spd.ellipse([ccx - R*0.5, ccy - R*0.78, ccx + R*0.18, ccy - R*0.30], fill=(255, 255, 255, 70))
spec = spec.filter(ImageFilter.GaussianBlur(26))
img.alpha_composite(spec)

img.save("icons/icon-1024.png")
for sz in (512, 192):
    img.resize((sz, sz), Image.LANCZOS).save(f"icons/icon-{sz}.png")
print("ok - icones gerados")

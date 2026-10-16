"""extraer_assets.py - Extrae los graficos de Spherical (ZX Spectrum 48K) de la cinta TZX ya troceada.
Uso: python3 -I extraer_assets.py dir_bloques(tape/) snapshot_base.sna dir_salida
  dir_bloques : salida de extraer_cinta.py (2_smc.bin, 4_0.bin ... 12_8.bin, 1_fadscr.bin, 3_border.bin)
  snapshot_base: aporta las tablas de silueta $5B00/$5C00 (las genera el codigo del juego al arrancar)
Salida: sprites/, tiles/, fuente/, hud/, pantallas/ + sprites.json + hojas (sheets).
Uso personal/educativo: son graficos con copyright (Rainbow Arts / Electronic Zoo); no redistribuir."""
import sys, os, json
from PIL import Image
tapedir, base, out = sys.argv[1:4]
smc = open(os.path.join(tapedir, '2_smc.bin'), 'rb').read()          # $6100..$F7FF
mem = bytearray(0x10000); mem[0x6100:0x6100+len(smc)] = smc
ram = open(base, 'rb').read()[27:]
T1 = ram[0x5B00-0x4000:0x5C00-0x4000]; T2 = ram[0x5C00-0x4000:0x5D00-0x4000]
worlds = {}
for w in range(9):
    f = [x for x in os.listdir(tapedir) if x.endswith('_%d.bin' % w) and x.split('_')[0].isdigit() and len(x.split('_')) == 2 and int(x.split('_')[0]) == 4+w]
    worlds[w] = open(os.path.join(tapedir, f[0]), 'rb').read()
for d in ('sprites/base', 'tiles', 'fuente', 'hud', 'pantallas'): os.makedirs(os.path.join(out, d), exist_ok=True)
PAL = [(0,0,0),(0,0,205),(205,0,0),(205,0,205),(0,205,0),(0,205,205),(205,205,0),(205,205,205)]
def col(c, br): return tuple(min(255, int(v*(1.2 if br else 1.0))) for v in PAL[c])

def sprite_rows(b):  # 32 bytes -> 16 filas de 16 bits
    return [(b[2*i] << 8) | b[2*i+1] for i in range(16)]
def sprite_png(b):
    """RGBA 16x16: silueta calculada igual que C384 (mascara = T1[byte izq]<<8 | T2[byte der]); tinta blanca, papel negro."""
    im = Image.new('RGBA', (16, 16), (0, 0, 0, 0)); raw = Image.new('RGBA', (16, 16), (0, 0, 0, 0))
    for y in range(16):
        g0, g1 = b[2*y], b[2*y+1]; g = (g0 << 8) | g1
        m = (T1[g0] << 8) | T2[g1]
        for x in range(16):
            bit = (g >> (15-x)) & 1
            if bit: raw.putpixel((x, y), (255, 255, 255, 255))
            if ((m >> (15-x)) & 1) == 0 or bit:
                im.putpixel((x, y), (255, 255, 255, 255) if bit else (0, 0, 0, 255))
    return im, raw
def tile_png(b36):
    bm, at = b36[:32], b36[32:36]; im = Image.new('RGB', (16, 16))
    for y in range(16):
        for x in range(16):
            bit = (bm[y*2 + x//8] >> (7 - x % 8)) & 1; a = at[(y//8)*2 + x//8]
            im.putpixel((x, y), col((a & 7) if bit else (a >> 3) & 7, (a >> 6) & 1))
    return im
def sheet(imgs, labels, cols, fn, scale=3, bg=(40, 40, 40)):
    from PIL import ImageDraw
    n = len(imgs); rows = (n+cols-1)//cols; W = 16*scale+6; H = 16*scale+16
    sh = Image.new('RGB', (cols*W, rows*H), bg); dr = ImageDraw.Draw(sh)
    for i, (im, lb) in enumerate(zip(imgs, labels)):
        ox, oy = (i % cols)*W+3, (i//cols)*H+12
        bgc = Image.new('RGB', (16, 16), (0, 0, 70)); bgc.paste(im.convert('RGBA'), (0, 0), im.convert('RGBA'))
        sh.paste(bgc.resize((16*scale, 16*scale), Image.NEAREST), (ox, oy)); dr.text((ox, oy-11), lb, fill=(255, 255, 0))
    sh.save(fn)

meta = {'sprites': [], 'tiles': [], 'notas': 'sprite = 16 filas x 2 bytes, 1 bit/pixel; direccion = $6100 + 32*frame; el color lo da el atributo del fondo (aqui: blanco)'}
# ---- sprites base (frames $00-$6F, bloque smc)
simgs, slab = [], []
for f in range(0x70):
    b = bytes(mem[0x6100+32*f:0x6100+32*f+32])
    im, raw = sprite_png(b)
    im.save(os.path.join(out, 'sprites/base/spr_%03X.png' % f)); raw.save(os.path.join(out, 'sprites/base/spr_%03X_raw.png' % f))
    open(os.path.join(out, 'sprites/base/spr_%03X.bin' % f), 'wb').write(b)
    meta['sprites'].append({'frame': f, 'mundo': 'base', 'direccion': '%04X' % (0x6100+32*f), 'vacio': not any(b), 'hex': b.hex()})
    simgs.append(im); slab.append('%02X' % f)
sheet(simgs, slab, 14, os.path.join(out, 'sprites/hoja_base.png'))
# ---- imagenes grandes (jefes / fondos) de cada mundo: tabla DABA, 8 bytes por mundo 1..8:
# ancho(bytes), alto(filas), direccion de datos (pares mascara,dato), destino en el bufer $DF72 (+29*y+x), 2 bytes sin identificar
grandes = {}
for w in range(1, 9):
    r = bytes(mem[0xDABA+(w-1)*8:0xDABA+w*8])
    if r[0]:
        a = r[2] | r[3] << 8
        grandes.setdefault(w, []).append((a, r[0], r[1], r[4] | r[5] << 8))
        if w == 3: grandes[w].append((0x7A78, 0x0C, 0x45, 0xE9D1))   # segunda imagen (parche en $CA83)
def en_grande(w, f):
    ad = 0x6100 + 32*f
    return any(a <= ad < a + c*h*2 for a, c, h, _ in grandes.get(w, []))
# ---- sprites propios de cada mundo (frames $70-$127: $6F00-$85FF del bloque del mundo)
seen = {}
for w, data in worlds.items():
    os.makedirs(os.path.join(out, 'sprites/mundo%d' % w), exist_ok=True)
    imgs, labs = [], []
    for f in range(0x70, 0x128):
        off = (f-0x70)*32; b = data[off:off+32]
        if len(b) < 32: continue
        eg = en_grande(w, f)                 # el fotograma cae dentro de una imagen grande (jefe): el juego lo dibuja igualmente como sprite de segmento
        if not any(b):                       # fotograma vacio: se anota en el json (el juego puede dibujarlo) pero no se guarda imagen
            meta['sprites'].append({'frame': f, 'mundo': w, 'direccion': '%04X' % (0x6100+32*f), 'vacio': True, 'en_imagen_grande': eg, 'hex': b.hex()}); continue
        im, raw = sprite_png(b)
        im.save(os.path.join(out, 'sprites/mundo%d/spr_%03X.png' % (w, f))); raw.save(os.path.join(out, 'sprites/mundo%d/spr_%03X_raw.png' % (w, f)))
        open(os.path.join(out, 'sprites/mundo%d/spr_%03X.bin' % (w, f)), 'wb').write(b)
        meta['sprites'].append({'frame': f, 'mundo': w, 'direccion': '%04X' % (0x6100+32*f), 'vacio': False, 'en_imagen_grande': eg, 'hex': b.hex()})
        imgs.append(im); labs.append('%03X' % f)
    if imgs: sheet(imgs, labs, 14, os.path.join(out, 'sprites/hoja_mundo%d.png' % w))
# ---- casillas
timgs, tlab = [], []
for c in range(0x5B):
    b = bytes(mem[0x9B00+36*c:0x9B00+36*c+36]); im = tile_png(b)
    im.save(os.path.join(out, 'tiles/tile_%02X.png' % c)); open(os.path.join(out, 'tiles/tile_%02X.bin' % c), 'wb').write(b)
    meta['tiles'].append({'codigo': c, 'conjunto': 'base', 'hex': b.hex()}); timgs.append(im); tlab.append('%02X' % c)
sheet(timgs, tlab, 12, os.path.join(out, 'tiles/hoja_casillas.png'))
alt = worlds[7][:0x2D0]                       # mundo 7: el nivel 70 las copia a $9E60 (casillas $18-$2B)
os.makedirs(os.path.join(out, 'tiles/mundo7_alt'), exist_ok=True); aimgs, alab = [], []
for i in range(20):
    b = alt[36*i:36*i+36]; im = tile_png(b); im.save(os.path.join(out, 'tiles/mundo7_alt/tile_%02X.png' % (0x18+i)))
    aimgs.append(im); alab.append('%02X' % (0x18+i)); meta['tiles'].append({'codigo': 0x18+i, 'conjunto': 'mundo7', 'hex': b.hex()})
sheet(aimgs, alab, 10, os.path.join(out, 'tiles/hoja_casillas_mundo7_alt.png'))
# ---- fuente 8x8 ($F592, ASCII-$20)
fimgs, flab = [], []
for c in range(0x20, 0x20+(0xF79B-0xF592)//8):
    b = bytes(mem[0xF592+(c-0x20)*8:0xF592+(c-0x20)*8+8]); im = Image.new('RGBA', (8, 8), (0, 0, 0, 0))
    for y in range(8):
        for x in range(8):
            if (b[y] >> (7-x)) & 1: im.putpixel((x, y), (255, 255, 255, 255))
    im.save(os.path.join(out, 'fuente/chr_%02X.png' % c)); fimgs.append(im); flab.append('%02X' % c)
from PIL import ImageDraw
cols = 16; rows = (len(fimgs)+cols-1)//cols; fs = Image.new('RGB', (cols*30, rows*34), (40, 40, 40)); fd = ImageDraw.Draw(fs)
for i, (im, lb) in enumerate(zip(fimgs, flab)):
    ox, oy = (i % cols)*30+3, (i//cols)*34+12
    bg = Image.new('RGB', (8, 8), (0, 0, 70)); bg.paste(im, (0, 0), im); fs.paste(bg.resize((24, 24), Image.NEAREST), (ox, oy)); fd.text((ox, oy-11), lb, fill=(255, 255, 0))
fs.save(os.path.join(out, 'fuente/hoja_fuente.png'))
# ---- HUD ($F492-$F591): filas de 2 bytes
hud = Image.new('RGB', (16, 128), (0, 0, 70))
for y in range(128):
    v = (mem[0xF492+2*y] << 8) | mem[0xF492+2*y+1]
    for x in range(16):
        if (v >> (15-x)) & 1: hud.putpixel((x, y), (255, 255, 255))
hud.resize((64, 512), Image.NEAREST).save(os.path.join(out, 'hud/hud_F492_F591.png'))
for i in range(8):   # 8 iconos de 16x16 (32 bytes cada uno): $F492 + 32*i
    hud.crop((0, 16*i, 16, 16*i+16)).resize((64, 64), Image.NEAREST).save(os.path.join(out, 'hud/hud_icono_%d.png' % i))
open(os.path.join(out, 'hud/hud_F492_F591.bin'), 'wb').write(bytes(mem[0xF492:0xF592]))
# ---- pantallas SCREEN$
def scr_png(data):
    im = Image.new('RGB', (256, 192))
    for y in range(192):
        base_a = ((y & 0xC0) << 5) | ((y & 7) << 8) | ((y & 0x38) << 2)
        for xb in range(32):
            b = data[base_a + xb]; a = data[6144 + (y//8)*32 + xb]
            ink, pap, br = a & 7, (a >> 3) & 7, (a >> 6) & 1
            for k in range(8): im.putpixel((xb*8+k, y), col(ink if (b >> (7-k)) & 1 else pap, br))
    return im
for nm, fn in (('carga', '1_fadscr.bin'), ('marco', '3_border.bin')):
    scr_png(open(os.path.join(tapedir, fn), 'rb').read()).save(os.path.join(out, 'pantallas/%s.png' % nm))
json.dump(meta, open(os.path.join(out, 'sprites.json'), 'w'), indent=1)
print('sprites', len(meta['sprites']), 'tiles', len(meta['tiles']))


# --- Pantalla final "The End" (128x64 px + atributos 16x8), dentro del bloque del mundo 8 en $9064 ---
def extraer_final(dir_bloques, salida):
    import glob, os
    f = glob.glob(os.path.join(dir_bloques, '12_8.bin'))
    if not f:
        return
    d = open(f[0], 'rb').read()   # bloque del mundo 8, empieza en $6F00
    o = 0x9064 - 0x6F00
    pix, att = d[o:o+1024], d[o+1024:o+1024+128]
    cols = [(0,0,0),(0,0,255),(255,0,0),(255,0,255),(0,255,0),(0,255,255),(255,255,0),(255,255,255)]
    im = Image.new('RGB', (128, 64))
    for y in range(64):
        for xb in range(16):
            b = pix[y*16+xb]; a = att[(y//8)*16+xb]
            for k in range(8):
                im.putpixel((xb*8+k, y), cols[a & 7] if (b >> (7-k)) & 1 else cols[(a >> 3) & 7])
    im.save(os.path.join(salida, 'pantallas', 'final_the_end.png'))
    open(os.path.join(salida, 'pantallas', 'final_the_end.bin'), 'wb').write(pix + att)

def extraer_jefes(salida):
    os.makedirs(os.path.join(salida, 'jefes'), exist_ok=True)
    for w, lst in grandes.items():
        for n, (a, c, h, dest) in enumerate(lst):
            d = worlds[w][a-0x6F00:a-0x6F00+c*h*2]
            im = Image.new('RGBA', (c*8, h), (0, 0, 0, 0))
            for y in range(h):
                for xb in range(c):
                    m, v = d[(y*c+xb)*2], d[(y*c+xb)*2+1]
                    for k in range(8):
                        if (v >> (7-k)) & 1: im.putpixel((xb*8+k, y), (255, 255, 255, 255))
                        elif not (m >> (7-k)) & 1: im.putpixel((xb*8+k, y), (0, 0, 0, 255))
            nm = 'jefe_mundo%d%s' % (w, 'ab'[n])
            im.save(os.path.join(salida, 'jefes', nm+'.png'))
            open(os.path.join(salida, 'jefes', nm+'.bin'), 'wb').write(d)
            meta.setdefault('imagenes_grandes', []).append({'mundo': w, 'archivo': nm, 'direccion': '%04X' % a, 'ancho_bytes': c, 'alto': h, 'destino_buffer': '%04X' % dest})

if __name__ == '__main__':
    extraer_final(sys.argv[1], sys.argv[3])
    extraer_jefes(sys.argv[3])
    json.dump(meta, open(os.path.join(sys.argv[3], 'sprites.json'), 'w'), indent=1)

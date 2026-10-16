"""extraer_niveles.py - Extrae del snapshot los niveles del MUNDO CARGADO (mundo 0) y los dibuja.
Formatos (verificados leyendo C563-C6C0 y comparando con capturas):
  mapas 1P : 8A60 + 140*n   (n=0..9)       mapas 2P : 8FD8 + 140*n
  fondo    : 4B00 + offset(2 bytes cabecera) -> 140 bytes = CAPA DE FONDO 14x10 (papel pintado), se copia a DEE6
  cabeceras: 9668.. 20 registros (10 de 1P y 10 de 2P) y luego los especiales.
     registro = fondo(2) esfera(x,y) P1(x,y) P2(x,y) n_enemigos(1) n*[x,y,tipo,frame]
Uso: python3 -I extraer_niveles.py snapshot.sna directorio_salida [mundo]
(el snapshot debe tener cargado el bloque del mundo en 6F00-9AFF; ver extraer_cinta.py)"""
import sys, json, os
from PIL import Image
snap, out = sys.argv[1], sys.argv[2]
world = int(sys.argv[3]) if len(sys.argv) > 3 else 0
os.makedirs(out, exist_ok=True)
d = bytearray(open(snap, 'rb').read()[27:])
if world == 7:   # nivel 70: C5D5-C5E1 copia 720 bytes de 6F00 a 9E60 (juego alternativo de casillas 18h-2Bh)
    d[0x9E60-0x4000:0x9E60-0x4000+0x2D0] = d[0x6F00-0x4000:0x6F00-0x4000+0x2D0]
m = lambda a, n=1: d[a-0x4000:a-0x4000+n]
PAL = [(0,0,0),(0,0,205),(205,0,0),(205,0,205),(0,205,0),(0,205,205),(205,205,0),(205,205,205)]
def col(c, br):
    f = 1.2 if br else 1.0
    return tuple(min(255, int(v*f)) for v in c)
def tile_img(code):
    base = 0x9B00 + 36*code
    bm = m(base, 32); at = m(base+32, 4)
    im = Image.new('RGB', (16, 16))
    for y in range(16):
        for x in range(16):
            bit = ((bm[y*2 + x//8]) >> (7 - x % 8)) & 1
            a = at[(y//8)*2 + x//8]
            ink, pap, br = a & 7, (a >> 3) & 7, (a >> 6) & 1
            im.putpixel((x, y), col(PAL[ink if bit else pap], br))
    return im
def tile_fg(code):
    """casilla con silueta (relleno entre el primer y el ultimo pixel de cada fila) sobre transparente"""
    base = 0x9B00 + 36*code
    bm = m(base, 32); at = m(base+32, 4)
    im = Image.new('RGBA', (16, 16), (0, 0, 0, 0))
    for y in range(16):
        bits = [((bm[y*2 + x//8]) >> (7 - x % 8)) & 1 for x in range(16)]
        if 1 not in bits: continue
        lo = bits.index(1); hi = 15 - bits[::-1].index(1)
        for x in range(lo, hi+1):
            a = at[(y//8)*2 + x//8]
            ink, pap, br = a & 7, (a >> 3) & 7, (a >> 6) & 1
            im.putpixel((x, y), col(PAL[ink if bits[x] else pap], br) + (255,))
    return im
cache = {}
def tile(c):
    if c not in cache: cache[c] = tile_img(c)
    return cache[c]
def headers():
    p = 0x9668; recs = []
    for i in range(22):
        h = m(p, 8); n = m(p+8)[0]
        en = [dict(x=m(p+9+4*k)[0], y=m(p+10+4*k)[0], tipo=m(p+11+4*k)[0], frame=m(p+12+4*k)[0]) for k in range(n)]
        recs.append(dict(dir=hex(p), fondo=h[0] | h[1] << 8, esfera=(h[2], h[3]), p1=(h[4], h[5]), p2=(h[6], h[7]), enemigos=en)); p += 9 + 4*n
    return recs
H = headers()
res = {'1P': [], '2P': []}
for modo, base, off in (('1P', 0x8A60, 0), ('2P', 0x8FD8, 10)):
    for n in range(10):
        mp = list(m(base + 140*n, 140)); h = H[off + n]
        floor = list(m(0x4B00 + h['fondo'], 140))
        gl = 10*world + n
        if modo and gl in (10, 20, 50): floor = [0x11 if gl == 10 else 0]*140   # C682-C6A3
        existe = gl <= 80 and gl != 79       # C524: el nivel $4E (78) salta a $50 (80); $51 (81) = fin del juego -> 79 y 81-89 no existen
        res[modo].append(dict(mundo=world, nivel_global=10*world+n, nivel_local=n, existe=existe, mapa=mp, **{k: h[k] for k in h if k!='suelo'}, fondo_datos=floor))
        if not existe: continue
        im = Image.new('RGBA', (14*16, 10*16))
        for i, c in enumerate(floor):
            im.paste(tile(c).convert('RGBA'), ((i % 14)*16, (i//14)*16))
        for i, c in enumerate(mp):
            if c == 0: continue
            t = tile_fg(c) if c in (0x41, 0x42, 0x43, 0x4C) else tile(c).convert("RGBA")
            im.alpha_composite(t, ((i % 14)*16, (i//14)*16))
        im = im.convert('RGB')
        im.save(os.path.join(out, 'mundo%d_%s_nivel%02d.png' % (world, modo, n)))
json.dump(res, open(os.path.join(out, 'mundo%d_niveles.json' % world), 'w'), indent=1)
# hoja resumen
sheet = Image.new('RGB', (2*(14*16+8), 10*(10*16+8)), (40, 40, 40))
for j, modo in enumerate(('1P', '2P')):
    for n in range(10):
        f = os.path.join(out, 'mundo%d_%s_nivel%02d.png' % (world, modo, n))
        if os.path.exists(f): sheet.paste(Image.open(f), (j*(14*16+8), n*(10*16+8)))
sheet.save(os.path.join(out, 'mundo%d_hoja_niveles.png' % world))
print('ok', len(res['1P']), len(res['2P']))
# ---- pantallas especiales (D39B=$42 -> mapa $9550 + cabecera 20 ; D39B=$57 -> mapa $95DC + cabecera 21)
esp = {}
for nom, base, idx in (('secreta42', 0x9550, 20), ('copa57', 0x95DC, 21)):
    mp = list(m(base, 140)); h = H[idx]
    floor = list(m(0x4B00 + h['fondo'], 140))
    im = Image.new('RGBA', (14*16, 10*16))
    for i, c in enumerate(floor): im.paste(tile(c).convert('RGBA'), ((i % 14)*16, (i//14)*16))
    for i, c in enumerate(mp):
        if c == 0: continue
        t = tile_fg(c) if c in (0x41, 0x42, 0x43, 0x4C) else tile(c).convert('RGBA')
        im.alpha_composite(t, ((i % 14)*16, (i//14)*16))
    im.convert('RGB').save(os.path.join(out, 'mundo%d_especial_%s.png' % (world, nom)))
    esp[nom] = dict(mapa=mp, **{k: h[k] for k in h if k != 'suelo'}, fondo_datos=floor)
json.dump(esp, open(os.path.join(out, 'mundo%d_especiales.json' % world), 'w'), indent=1)

"""manifiesto_sprites.py - convierte el volcado crudo de sprites (sprites.json) en un conjunto REUTILIZABLE:
  * manifiesto_sprites.json : cada fotograma con su tipo, su USO REAL (qué entidad lo dibuja, en qué mundos), su máscara de silueta y su posición en el atlas.
  * atlas_<grupo>.png       : atlas RGBA 1x (tinta blanca sobre transparente; recolorable) y atlas_<grupo>_silueta.png (interior de la silueta en negro).
  * manifiesto_sprites.md    : tabla legible (rol -> fotogramas) y explicación de los fotogramas vacíos / que no son sprites.
Entradas: sprites.json, ficheros de roles (mundo rol fotograma modo; los escribe keytrace.py con ROLES=...), jefes_animacion.json y un snapshot (tablas de máscara $5B00/$5C00).
Máscara = la que usa $C384: opaco = NOT tabla_A[byte izq] (8 bits) y NOT tabla_B[byte der] (8 bits); pixel con tinta = bit del gráfico.
Uso: python3 -I manifiesto_sprites.py sprites.json jefes_animacion.json snapshot.sna salida_dir roles1.txt [roles2.txt ...]"""
import sys, json, os, collections
from PIL import Image
sj, bj, snap, out = sys.argv[1:5]; rolfiles = sys.argv[5:]
os.makedirs(out, exist_ok=True)
J = json.load(open(sj)); B = json.load(open(bj))
mem = open(snap, 'rb').read()[27:]
TA = mem[0x5B00-0x4000:0x5C00-0x4000]; TB = mem[0x5C00-0x4000:0x5D00-0x4000]

# ---- uso real: (mundo, rol, fotograma) -> mundos donde sale
uso = collections.defaultdict(lambda: collections.defaultdict(set))      # (clave_fotograma) -> rol -> {mundos}
for fn in rolfiles:
    for l in open(fn):
        if not l.strip(): continue
        w, rol, fr, modo = l.split(); w = int(w); fr = int(fr)
        if rol.startswith('orbe') and fr not in (0x3A, 0x3B, 0x3C): continue      # $45/$FF = valor residual del registro antes de que $B099 lo inicialice (orbe45.py), no un gráfico del orbe
        clave = ('base', fr) if fr < 0x70 else (w, fr)
        uso[clave][rol].add(w)
# la maga (J2) se dibuja como fotograma de J1 + $0D: los fotogramas $0D-$19 son suyos (comprobado en $C318 y con rolesextra.py)

# ---- regiones especiales de cada mundo (no son sprites 16x16)
def en_imagen(w, f):
    s0 = 0x6100 + 32*f
    for im in J['imagenes_grandes']:
        if im['mundo'] == w:
            a = int(im['direccion'], 16); n = 2*im['ancho_bytes']*im['alto']       # pares (mascara, dato)
            if a < s0+32 and a+n > s0: return im['archivo']
    return None
def pose_de_jefe(w, f):
    b = B.get(str(w))
    if not b: return None
    n = len(b['segmentos'])
    for p in b['poses']:
        if p <= f < p+n: return 'pose %d (segmento %d de %d)' % (p, f-p, n)
    return None

def mascara(b):                       # 16 filas de 2 bytes -> lista de 16 enteros de 16 bits (1 = opaco)
    return [((~TA[b[2*y]] & 0xFF) << 8) | (~TB[b[2*y+1]] & 0xFF) for y in range(16)]

def nombre_grupo(clave):
    m, f = clave
    if m == 'base':
        if f <= 0x0C or f in (0x38, 0x39): return 'mago'   # $38/$39 = el mago bebiendo la poción ($ABF5 escribe en D3A9)
        if f <= 0x19: return 'maga'
        if f <= 0x23: return 'esfera'
        if f in (0x3A, 0x3B, 0x3C): return 'orbe'
        if f <= 0x39 or 0x3D <= f <= 0x6F or f == 0x3A: return 'enemigos'
        return 'otros'
    return 'jefes_mundo%d' % m

entradas = []; grupos = collections.defaultdict(list)
for s in J['sprites']:
    m = s['mundo'] if s['mundo'] == 'base' else int(s['mundo']); f = s['frame']; clave = (m, f)
    e = {'id': ('base_%02X' % f) if m == 'base' else 'w%d_%03X' % (m, f), 'mundo': m, 'frame': f, 'direccion': s['direccion']}
    if s['vacio']:
        e['tipo'] = 'vacio'; e['nota'] = 'todo ceros: relleno / fotograma reservado'
        if uso.get(clave): e['dibujado_por'] = {r: sorted(w) for r, w in uso[clave].items()}; e['nota'] = 'dibujado por el juego pero en blanco (borrado/parpadeo): se conserva'
        entradas.append(e); continue
    img = en_imagen(m, f) if m != 'base' else None
    if m != 'base' and m == 7 and f <= 0x86: e['tipo'] = 'casillas_nivel70'; e['nota'] = 'NO es sprite: 20 casillas alternativas ($18-$2B, 36 B cada una) que $C5E6 copia a $9E60 en el nivel 70'
    elif m == 8 and f >= 0xFC: e['tipo'] = 'atributos_jefe8'; e['nota'] = 'NO es sprite: tabla de atributos que copia $CAEA para el jefe del mundo 8'
    elif img and not uso.get(clave): e['tipo'] = 'imagen_grande'; e['nota'] = 'trozo de %s (pares máscara,dato; ver assets/jefes)' % img
    else:
        e['tipo'] = 'sprite'
        if uso.get(clave): e['dibujado_por'] = {r: sorted(w) for r, w in uso[clave].items()}
        p = pose_de_jefe(m, f) if m != 'base' else None
        if p: e['jefe'] = p
        if m == 'base' and not uso.get(clave) and 0x0D <= f <= 0x19: e['dibujado_por'] = {'J2': 'todos'}
        e['grupo'] = nombre_grupo(clave)
        b = bytes.fromhex(s['hex']); e['hex_grafico'] = s['hex']; e['hex_opaco'] = ''.join('%04X' % v for v in mascara(b))
        grupos[e['grupo']].append((e, b))
        if not e.get('dibujado_por') and 'jefe' not in e: e['nota'] = 'extraído pero no observado dibujado (ver md)'
    entradas.append(e)

# ---- atlas por grupo
def pintar(b, silueta):
    im = Image.new('RGBA', (16, 16), (0, 0, 0, 0)); op = mascara(b)
    for y in range(16):
        for x in range(16):
            ink = (b[2*y + x//8] >> (7 - x % 8)) & 1
            if ink: im.putpixel((x, y), (255, 255, 255, 255))
            elif silueta and (op[y] >> (15 - x)) & 1: im.putpixel((x, y), (0, 0, 0, 255))
    return im
for g, lst in grupos.items():
    cols = min(16, len(lst)); rows = (len(lst)+cols-1)//cols
    for suf, sil in (('', False), ('_silueta', True)):
        at = Image.new('RGBA', (cols*16, rows*16), (0, 0, 0, 0))
        for i, (e, b) in enumerate(lst):
            at.paste(pintar(b, sil), ((i % cols)*16, (i//cols)*16))
            if not sil: e['atlas'] = {'archivo': 'atlas_%s.png' % g, 'x': (i % cols)*16, 'y': (i//cols)*16, 'w': 16, 'h': 16}
        at.save(os.path.join(out, 'atlas_%s%s.png' % (g, suf)))

# ---- salida
cnt = collections.Counter(e['tipo'] for e in entradas)
json.dump({'nota': 'Sprite 16x16, 1 bit por pixel; el color lo pone el atributo de la casilla donde se dibuja. hex_opaco = silueta (16 filas de 16 bits) '
           'usada por la rutina $C384. La maga (J2) = fotogramas del mago + $0D. Uso personal/educativo: los gráficos son propiedad de sus autores.',
           'resumen': dict(cnt), 'fotogramas': entradas}, open(os.path.join(out, 'manifiesto_sprites.json'), 'w'), indent=1)

L = ['# Manifiesto de sprites', '', 'Generado con `manifiesto_sprites.py`. Todo el uso (qué entidad dibuja cada fotograma) viene de ejecutar el juego: barrido de los 90 niveles en modos 1P y 2P + `rolesextra.py`.', '',
     '| tipo | fotogramas |', '|---|---|'] + ['| %s | %d |' % (k, v) for k, v in sorted(cnt.items())] + ['']
rol = collections.defaultdict(lambda: collections.defaultdict(set))
for e in entradas:
    for r, w in (e.get('dibujado_por') or {}).items():
        for ww in (w if isinstance(w, list) else []): rol[r][e['id']].add(ww)
        if w == 'todos': rol[r][e['id']].add('todos')
L += ['## Fotogramas por entidad', '', '| entidad | fotogramas (id) | mundos |', '|---|---|---|']
for r in sorted(rol):
    ids = sorted(rol[r]); mundos = sorted(set().union(*rol[r].values()), key=str)
    pm = collections.defaultdict(list)
    for i in ids:
        if not i.startswith('base_'): pm[i.split('_')[0][1:]].append(i.split('_')[1])
    txt = ' '.join(i.replace('base_', '') for i in ids if i.startswith('base_'))
    if pm: txt += ' · propios de mundo: ' + '; '.join('mundo %s: %s' % (w, (v[0] + '-' + v[-1] + ' (%d)' % len(v)) if len(v) > 3 else ' '.join(v)) for w, v in sorted(pm.items()))
    L.append('| %s | %s | %s |' % (r, txt, ' '.join(map(str, mundos))))
L += ['', 'Notas: `J1` = mago, `J2` = maga (mago+$0D), `enemigoNN` = tipo NN del registro de enemigo (+8); tipo $12 y superiores = segmentos de jefe. '
      'El fotograma $46 aparece en varios tipos: es la boca cerrada de los lanzadores 5/6 y 0F-11 (no es un gráfico distinto por entidad).', '']
vac = [e for e in entradas if e['tipo'] == 'vacio']
dib = [e for e in vac if e.get('dibujado_por')]
L += ['## Fotogramas vacíos', '', '%d de %d entradas están a cero: son huecos del bloque (las regiones reservadas por mundo son mayores que los gráficos que contienen, y el bloque base tiene fotogramas sin usar).' % (len(vac), len(entradas)), '',
      'El juego SÍ dibuja %d fotogramas en blanco: %s. `base_46` es el fotograma "invisible" (reposo de los lanzadores 5/6 y 0F-11 y del enemigo 4); los `wN_xxx` son segmentos de pose de jefe que quedan vacíos en esa pose (el jefe no ocupa toda su cuadrícula). Se conservan porque son parte de la animación.' % (len(dib), ', '.join(e['id'] for e in dib)), '']
sn = [e for e in entradas if e['tipo'] == 'sprite' and not e.get('dibujado_por') and 'jefe' not in e]
L += ['## Sprites extraídos pero no observados dibujados', '', ', '.join(e['id'] for e in sn) or 'ninguno', '']
open(os.path.join(out, 'manifiesto_sprites.md'), 'w').write('\n'.join(L) + '\n')
print(dict(cnt)); print('grupos:', {g: len(v) for g, v in grupos.items()}); print('sin uso:', [e['id'] for e in sn])

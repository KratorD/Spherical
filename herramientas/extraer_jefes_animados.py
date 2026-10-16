"""extraer_jefes_animados.py - ensambla los jefes (tipos >= $12) pose a pose.
Uso: python3 -I extraer_jefes_animados.py dir_cinta(tape/) snapshot.sna dir_niveles_json(out_w/) salida
Formato (leido en $BDFA y $C864, ver spherical_anotado.ctl):
  * la tabla $DABA da, por mundo, un puntero (bytes +6/+7) a la tabla de animacion del jefe (terminada en $FF);
  * cada entrada de la tabla es el frame de la CABEZA; el segmento k del jefe usa el frame cabeza+k;
  * las posiciones (x,y) de cada segmento estan en la cabecera del nivel (registros enemigo, tipo >= $12).
"""
import sys, os, json
from PIL import Image
tape, snap, jdir, out = sys.argv[1:5]
os.makedirs(out, exist_ok=True)
ram = open(snap, 'rb').read()[27:]
mem = lambda a, n=1: ram[a-0x4000:a-0x4000+n]
T1, T2 = mem(0x5B00, 256), mem(0x5C00, 256)
smc = open(os.path.join(tape, '2_smc.bin'), 'rb').read()
def sprite(world_blk, f):
    if f < 0x70: b = smc[0x6100+32*f-0x6100:0x6100+32*f-0x6100+32]
    else: b = world_blk[(f-0x70)*32:(f-0x70)*32+32]
    return b
def draw(im, b, x, y):
    for r in range(16):
        g0, g1 = b[2*r], b[2*r+1]; g = g0 << 8 | g1; m = T1[g0] << 8 | T2[g1]
        for c in range(16):
            bit = (g >> (15-c)) & 1
            if bit: im.putpixel((x+c, y+r), (255, 255, 255))
            elif not (m >> (15-c)) & 1: im.putpixel((x+c, y+r), (0, 0, 0))
res = {}
for w in range(1, 9):
    ptr = mem(0xDABA+(w-1)*8+6, 2); ptr = ptr[0] | ptr[1] << 8
    if not ptr: continue
    tab = []; p = ptr
    while mem(p)[0] != 0xFF: tab.append(mem(p)[0]); p += 1
    lv = json.load(open(os.path.join(jdir, 'mundo%d_niveles.json' % w)))['1P'][0]
    boss = [e for e in lv['enemigos'] if e['tipo'] >= 0x12]
    blk = open(os.path.join(tape, '%d_%d.bin' % (4+w, w)), 'rb').read()
    poses = sorted(set(tab))
    res[w] = dict(tabla='%04X' % ptr, secuencia=tab, poses=poses, segmentos=[(e['x'], e['y'], e['tipo'], e['frame']) for e in boss])
    sheet = Image.new('RGB', (224*min(len(poses), 2), 160*((len(poses)+1)//2)), (0, 0, 120))
    for i, f in enumerate(poses):
        k = 0
        for e in boss:
            draw(sheet, sprite(blk, f+k), (i % 2)*224 + min(e['x']*2, 208), (i//2)*160 + min(e['y'], 144)); k += 1
    sheet.resize((sheet.width, sheet.height), Image.NEAREST).save(os.path.join(out, 'jefe_poses_mundo%d.png' % w))
json.dump(res, open(os.path.join(out, 'jefes_animacion.json'), 'w'), indent=1)
print({w: (r['tabla'], len(r['poses']), len(r['segmentos'])) for w, r in res.items()})

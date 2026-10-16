"""colortest.py - verifica el dibujado de niveles: para cada nivel de cada mundo carga mapa y fondo en el simulador, llama a #R$C9F5 (dibujar nivel)
y compara los atributos y los píxeles del búfer con lo que predice extraer_niveles.py (capa de fondo + mapa, con silueta en 0/41/42/43/4C).
Uso: python3 -I colortest.py dir_cinta(tape/) dir_json(out_w/)"""
import sys, json, os
sys.path.insert(0, '/home/claude/tools')
from keytrace import *
tape, jdir = sys.argv[1:3]
MASK = {0x00, 0x41, 0x42, 0x43, 0x4C}
tot = bad_a = bad_p = 0; resumen = []
for w in range(9):
    d = json.load(open(os.path.join(jdir, 'mundo%d_niveles.json' % w)))
    for modo in ('1P', '2P'):
        for lv in d[modo]:
            gl = lv['nivel_global']
            if not lv.get('existe', True): continue          # 79 (saltado por C537) y 81-89 no existen
            if gl % 10 == 0 and gl > 0: continue          # niveles de jefe: dibujan además una imagen grande
            sim = load(os.path.join(tape, 'mundo%d.sna' % w)); mem, reg, ops = sim.memory, sim.registers, sim.opcodes
            if w == 7:                                      # intercambio de casillas del nivel 70
                for i in range(0x2D0): mem[0x9E60+i] = mem[0x6F00+i]
            mem[0xD39A] = gl; mem[0xD98B] = w; mem[0xD39B] = 0; mem[0xDC3A] = 0
            for i, c in enumerate(lv['mapa']): mem[0xDE5A+i] = c
            for i, c in enumerate(lv['fondo_datos']): mem[0xDEE6+i] = c
            for i in range(160*29): mem[0xDF72+i] = 0
            reg[24] = 0xC9F5; reg[12] = 0xFFFC; mem[0xFFFC] = 0xF0; mem[0xFFFD] = 0xFF
            n = 0
            while reg[24] != 0xFFF0 and n < 3000000: ops[mem[reg[24]]](); n += 1
            fgs, bgs = lv['mapa'], lv['fondo_datos']
            tile_attr = lambda c: [mem[0x9B00+36*c+32+k] & 0x7F for k in range(4)]
            tile_bits = lambda c: [mem[0x9B00+36*c+k] for k in range(32)]
            for i in range(140):
                f, b = fgs[i], bgs[i]
                col, row = i % 14, i // 14
                src = b if f in MASK else f
                ea = tile_attr(src)
                aa = [mem[0xF1D4 + (2*row)*32 + 2*col], mem[0xF1D4 + (2*row)*32 + 2*col + 1], mem[0xF1D4 + (2*row+1)*32 + 2*col], mem[0xF1D4 + (2*row+1)*32 + 2*col + 1]]
                tot += 1
                if aa != ea: bad_a += 1; resumen.append(('attr', w, modo, gl, i, aa, ea))
                if f not in MASK:
                    eb = tile_bits(f)
                    pb = []
                    for y in range(16): pb += [mem[0xDF72 + (16*row+y)*29 + 2*col], mem[0xDF72 + (16*row+y)*29 + 2*col + 1]]
                    if pb != eb: bad_p += 1; resumen.append(('pix', w, modo, gl, i))
    print('mundo', w, 'comprobado; atributos distintos hasta ahora:', bad_a, 'pixeles distintos:', bad_p, flush=True)
print('celdas comprobadas', tot, '| atributos distintos', bad_a, '| píxeles distintos', bad_p)
import collections
print(sorted(collections.Counter((r[1],r[3],r[0]) for r in resumen).items()))
for r in resumen[:6]: print(r)

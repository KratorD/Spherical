"""verificar_mascara.py - compara la silueta/tinta que deduce manifiesto_sprites.py (tablas $5B00/$5C00) con el resultado REAL de la rutina $C384 del juego:
se rellena el bufer de fondo ($DF72) con $FF, se dibuja cada fotograma con x alineado (x AND 3 = 0) y se comprueba pixel a pixel (bit 1 = fondo o tinta; 0 = silueta sin tinta).
Uso: python3 -I verificar_mascara.py manifiesto_sprites.json dir_snapshots(tape/) snapshot_base.sna"""
import sys, json, os; sys.path.insert(0, '/home/claude/tools')
from keytrace import *
man = json.load(open(sys.argv[1]))['fotogramas']; tape = sys.argv[2]; basesna = sys.argv[3]
ok = bad = 0; malos = []
def probar(snap, lst):
    global ok, bad
    sim = load(snap); tr = KeyTracer(); sim.set_tracer(tr); mem, reg, ops = sim.memory, sim.registers, sim.opcodes
    for e in lst:
        for i in range(29*160): mem[0xDF72+i] = 0xFF
        ix = 0xD3F8; mem[ix] = 8; mem[ix+1] = 20; mem[ix+2] = e['frame'] & 0xFF; mem[ix+3] = 0x00; mem[ix+4] = 0xFB
        reg[8] = ix >> 8; reg[9] = ix & 255; reg[24] = 0xC384; reg[12] = 0xFFF0 - 2; mem[0xFFEE] = 0xF0; mem[0xFFEF] = 0xFF
        # los fotogramas >= $100 no caben en el byte de frame: se omiten (solo mundo 8: $100-$102 son atributos)
        n = 0
        while reg[24] != 0xFFF0 and n < 20000: ops[mem[reg[24]]](); n += 1
        g = bytes.fromhex(e['hex_grafico']); op = [int(e['hex_opaco'][4*y:4*y+4], 16) for y in range(16)]
        base = 0xDF72 + 20*29 + 8//4
        fallo = False
        for y in range(16):
            real = (mem[base+29*y] << 8) | mem[base+29*y+1]
            ink = (g[2*y] << 8) | g[2*y+1]
            esperado = (~op[y] & 0xFFFF) | ink
            if real != esperado: fallo = True
        if fallo: bad += 1; malos.append(e['id'])
        else: ok += 1
probar(basesna, [e for e in man if e['tipo'] == 'sprite' and e['mundo'] == 'base'])
for w in range(1, 9):
    lst = [e for e in man if e['tipo'] == 'sprite' and e['mundo'] == w and e['frame'] < 0x100]
    if lst: probar(os.path.join(tape, 'mundo%d.sna' % w), lst)
print('sprites coinciden con el dibujo real de $C384: %d | no coinciden: %d %s' % (ok, bad, malos[:20]))

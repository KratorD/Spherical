"""despachotest.py - demuestra POR EJECUCION que $B8A8 es inalcanzable: se entra en el despachador de enemigos ($B836) con los 256 valores posibles
del tipo (+8), con y sin congelación, y se sigue la cadena de comparaciones hasta salir de ella (pc fuera de $B836-$B8A8). Uso: python3 -I despachotest.py nivel2.sna"""
import sys; sys.path.insert(0, '/home/claude/tools')
from keytrace import *
destinos = {}; alcanza = []
for freeze in (0, 4):
    for t in range(256):
        sim = load(sys.argv[1]); tr = KeyTracer(); sim.set_tracer(tr); mem, reg, ops = sim.memory, sim.registers, sim.opcodes
        mem[0xD3F8] = 0x30; mem[0xD3F9] = 0x30; mem[0xD400] = t; mem[0xD3BC] = freeze; mem[0xD3D9] = 0
        reg[10] = 0xD3; reg[11] = 0xF8; reg[12] = 0xFFE0; reg[24] = 0xB836; reg[2] = 1
        n = 0
        while 0xB836 <= reg[24] <= 0xB8A8 and n < 100:
            if reg[24] == 0xB8A8: alcanza.append((freeze, t))
            ops[mem[reg[24]]](); n += 1
        destinos.setdefault(reg[24], []).append(t)
print('valores de tipo (x2 modos) que ejecutan $B8A8:', alcanza or 'ninguno')
for d, ts in sorted(destinos.items()): print('  salida a $%04X: tipos %s' % (d, ('%02X-%02X (%d)' % (min(ts), max(ts), len(ts))) if len(ts) > 4 else ts))

"""energiatest.py - ejecuta la rutina de energia $CDF5 (con IY = registro del jugador) para comprobar sus ramas:
C=$FF con energia 0 -> $CE12 (satura a 0); C=$FF con energia 50 -> 49; C=+10 con 95 -> $CE03-$CE0A (satura a 100, rama SIN llamadores reales).
Uso: python3 -I energiatest.py nivel2.sna"""
import sys; sys.path.insert(0, '/home/claude/tools')
from keytrace import *
snap = sys.argv[1]
for e, c in ((0, 0xFF), (50, 0xFF), (95, 10), (3, 5)):
    sim = load(snap); tr = KeyTracer(); sim.set_tracer(tr); mem, reg, ops = sim.memory, sim.registers, sim.opcodes
    mem[0xD3EF] = e; mem[0xD3BC] &= ~2
    reg[10] = 0xD3; reg[11] = 0xA7; reg[3] = c; reg[24] = 0xCDF5; reg[12] = 0xFFF0; mem[0xFFF0] = 0xF0; mem[0xFFF1] = 0xFF
    vis = set(); n = 0
    while reg[24] != 0xFFF0 and n < 2000: vis.add(reg[24]); ops[mem[reg[24]]](); n += 1
    print('energia %3d + C=%02X -> %3d | $CE03:%s $CE12:%s' % (e, c, mem[0xD3EF], 0xCE03 in vis, 0xCE12 in vis))

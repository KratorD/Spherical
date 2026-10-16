"""ultimos.py - ejecuta directamente, con el estado preparado, las ultimas ramas que las partidas no alcanzan:
 $B73A  (salto hacia arriba chocando con el techo: fase<8 y E bit0=0)
 $BEE5  (bloque agachado fuera de la ultima fila)
 $BA88  (proyectil que sale de pantalla)  y  $C272 (esfera subiendo con D91F negativo sobre la casilla $44)
Uso: python3 -I ultimos.py nivel2.sna"""
import sys, itertools; sys.path.insert(0, '/home/claude/tools')
from keytrace import *
snap = sys.argv[1]
def nuevo():
    sim = load(snap); tr = KeyTracer(); sim.set_tracer(tr); return sim, sim.memory, sim.registers, sim.opcodes
def correr(ops, mem, reg, pc, n=6000, stop=0xFFF0, vis=None):
    vis = set() if vis is None else vis
    reg[24] = pc; reg[12] = 0xFFF0 - 2; mem[0xFFEE] = 0xF0; mem[0xFFEF] = 0xFF
    k = 0
    while reg[24] != stop and k < n: vis.add(reg[24]); ops[mem[reg[24]]](); k += 1
    return vis
# --- B73A: jugador subiendo (fase 3) con techo
hit = False
for fase, y, x in itertools.product((1, 3, 5, 7), (0x40, 0x50, 0x60, 0x70), (24, 25, 32)):
    for fill in (0x48, 0x01, 0x30):
        sim, mem, reg, ops = nuevo()
        for i in range(140): mem[0xDE5A+i] = 0
        for i in range(140):
            if i // 14 == (y >> 4) - 1: mem[0xDE5A+i] = fill
        mem[0xD3A7] = x; mem[0xD3A8] = y; mem[0xD3A9] = 0; mem[0xD3B0] = fase; reg[10] = 0xD3; reg[11] = 0xA7
        v = correr(ops, mem, reg, 0xB6FE)
        if 0xB73A in v: print('B73A alcanzado: fase', fase, 'y', hex(y), 'x', x, 'relleno', hex(fill)); hit = True; break
    if hit: break
if not hit: print('B73A no alcanzado en la rejilla probada')
# --- BEE5: bloque agachado (frame >= $0B) con y = $80
sim, mem, reg, ops = nuevo()
mem[0xD3A7] = 24; mem[0xD3A8] = 0x80; mem[0xD3A9] = 0x0B; mem[0xD3AE] = 1; mem[0xD98A] = 0x10; mem[0xD91E] = 1; mem[0xD3B1] = 0; mem[0xD3BC] &= 0x7F
reg[10] = 0xD3; reg[11] = 0xA7
antes = bytes(mem[0xDE5A:0xDE5A+140])
v = correr(ops, mem, reg, 0xBE7B)
print('BEE5 alcanzado:', 0xBEE5 in v, '| celdas del mapa cambiadas:', [i for i in range(140) if mem[0xDE5A+i] != antes[i]])
# --- BA88: lanzador de proyectiles tipo 5 con el proyectil a punto de salir de pantalla
sim, mem, reg, ops = nuevo()
mem[0xD3F8] = 0x50; mem[0xD3F9] = 0x30; mem[0xD3FF] = 14; mem[0xD400] = 5; mem[0xD989] = 1
reg[10] = 0xD3; reg[11] = 0xF8; reg[0] = 5
v = correr(ops, mem, reg, 0xBA25, stop=0xBE70)
print('BA88 alcanzado:', 0xBA88 in v, '| +7 tras la rutina =', mem[0xD3FF])
# --- C272: esfera subiendo (D91F negativo) justo debajo de la casilla de salida $44; con D91F positivo no debe activarse
for vy in (0xFC, 0x04):
    sim, mem, reg, ops = nuevo()
    mem[0xD3F0] = 40; mem[0xD3F1] = 0x50; mem[0xD91F] = vy
    for i in range(140): mem[0xDE5A+i] = 0
    mem[0xDE5A + (0x50 >> 4)*14 + 40//8 - 14] = 0x44
    reg[10] = 0xD3; reg[11] = 0xF0
    v = correr(ops, mem, reg, 0xC19C)
    print('C19C con D91F=%02X: D (toca salida) = %d | $C272 ejecutado: %s' % (vy, reg[4], 0xC272 in v))

"""menuyfin.py - (a) detección del joystick Kempston en el arranque ($A83A-$A844 y D988), (b) tecla 7 dos veces (claro -> oscuro -> claro, $AA72) y tecla 6 (mejores
puntuaciones) volviendo al menú ($AA5A), (c) fin de partida en el nivel 70: se restauran las casillas del mundo 7 ($AD37).
Uso: python3 -I menuyfin.py menu.sna"""
import sys; sys.path.insert(0, '/home/claude/tools')
import keytrace
from keytrace import *
keytrace.KEYS.update({'6': (0xEF, 4), '7': (0xEF, 3)})
snap = sys.argv[1]
def bucle(sim, tr, frames, keys, parar=None):
    mem, reg, ops = sim.memory, sim.registers, sim.opcodes
    fd, ia = sim.frame_duration, sim.int_active
    t = reg[25]; nxt = ((t+fd-ia)//fd)*fd; frame = 0; vis = set(); n = 0
    while frame < frames and n < 60000000:
        pc = reg[24]; vis.add(pc); ops[mem[pc]](); n += 1
        if parar and parar(pc): break
        t = reg[25]
        if t >= nxt:
            if t < nxt+ia:
                if reg[26] and sim.accept_interrupt(reg, mem, pc): frame += 1; nxt += fd; tr.pressed = keys(frame)
            else: nxt += fd
    return vis, frame
# (a) detección de Kempston: IN A,($1F) devuelve < $20 durante 10000 lecturas
sim = load(snap); tr = KeyTracer(); sim.set_tracer(tr); tr.kemp = 0
mem, reg = sim.memory, sim.registers
reg[24] = 0xA834; reg[12] = 0xFFFC; mem[0xFFFC] = 0xF0; mem[0xFFFD] = 0xFF; reg[0] = 0
vis, f = bucle(sim, tr, 30, lambda f: set(), parar=lambda pc: pc == 0xA84B)
print('a) Kempston presente: D988 =', mem[0xD988], '(1 = hay joystick) | pasa por $A841-$A844:', 0xA841 in vis)
# (b) tecla 7 dos veces y tecla 6
sim = load(snap); tr = KeyTracer(); sim.set_tracer(tr); mem = sim.memory
ks = lambda f: {'7'} if 150 <= f < 215 else ({'7'} if 260 <= f < 330 else ({'6'} if 380 <= f < 440 else ({'SPACE'} if 520 <= f < 560 else set())))
registro = []
vis, f = bucle(sim, tr, 700, ks)
print('b) F79B final =', mem[0xF79B], '(1 tras dos pulsaciones) | $AA72 (oscuro -> claro):', 0xAA72 in vis, '| $AA5A (vuelve al menú tras las puntuaciones):', 0xAA5A in vis)
# (c) fin de partida en el nivel 70
sim = load(snap); tr = KeyTracer(); sim.set_tracer(tr); mem, reg = sim.memory, sim.registers
mem[0xD39A] = 70; mem[0xD98B] = 7
for i in range(0x2D0): mem[0x71D0+i] = (i * 7) & 255          # copia de seguridad ficticia de las casillas originales
reg[24] = 0xACEE; reg[12] = 0xFFFE; reg[26] = 1
vis, f = bucle(sim, tr, 900, lambda f: {'SPACE'} if f % 30 < 6 else {'ENTER'} if f % 30 in range(12, 18) else set(), parar=lambda pc: pc == 0xAD42)
print('c) fin de partida en el nivel 70: $AD37 (restaura casillas):', 0xAD37 in vis, '| $9E60 == copia de $71D0:', bytes(mem[0x9E60:0x9E60+0x2D0]) == bytes(mem[0x71D0:0x71D0+0x2D0]))

"""casillatest.py - comprueba en el simulador las casillas $3F (pergamino) y $40 (copa): se coloca la casilla bajo el jugador 1 y se registran las rutas ejecutadas.
Uso: python3 -I casillatest.py nivel2.sna"""
import sys; sys.path.insert(0, '/home/claude/tools')
from keytrace import *
def run(tile, nivel, watch, frames=90, keys=lambda f: set()):
    sim = load(sys.argv[1]); tr = KeyTracer(); sim.set_tracer(tr)
    mem, reg, ops = sim.memory, sim.registers, sim.opcodes
    mem[0xD39A] = nivel
    mem[0xDE5A + 17] = tile            # casilla bajo el jugador 1 (x=24,y=16)
    mem[0xD3A7] = 24; mem[0xD3A8] = 16
    fd, ia = sim.frame_duration, sim.int_active
    t = reg[25]; nxt = ((t+fd-ia)//fd)*fd; frame = 0; hit = {}
    while frame < frames:
        pc = reg[24]
        if pc in watch: hit.setdefault(watch[pc], frame)
        ops[mem[pc]]()
        t = reg[25]
        if t >= nxt:
            if t < nxt+ia:
                if reg[26] and sim.accept_interrupt(reg, mem, pc): frame += 1; nxt += fd; tr.pressed = keys(frame)
            else: nxt += fd
    return hit, mem
w = {0xB572: 'pergamino: clave encontrada para el nivel', 0xB586: 'pergamino: espera tecla', 0xB5A0: 'recoger casilla (fin)', 0xB527: 'copa $40', 0xB542: 'copa: D39B=$57'}
for nivel, label in ((12, 'nivel 12 (RADAGAST)'), (21, 'nivel 21 (YARMAK)'), (19, 'nivel 19 (ninguna)')):
    h, m = run(0x3F, nivel, w, keys=lambda f: {'SPACE'} if 40 <= f < 50 else set())
    print('casilla $3F,', label, '->', h)
h, m = run(0x40, 5, w, frames=200, keys=lambda f: {'SPACE'} if 90 <= f < 110 else set())
print('casilla $40 ->', h, '| D39B =', hex(m[0xD39B]), '| D39A =', m[0xD39A])

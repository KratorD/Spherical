"""teclasjuego.py - teclas especiales dentro del juego: M / N (con la clave ILLUMINATUS, D079<>0) = nivel siguiente / anterior, H = pausa (atributos a azul oscuro y vuelta),
T = reinicia D920 a $0101 (si era <> 0).
Uso: python3 -I teclasjuego.py nivel2.sna"""
import sys; sys.path.insert(0, '/home/claude/tools')
import keytrace
from keytrace import *
keytrace.KEYS.update({'m': (0x7F, 2), 'n': (0x7F, 3), 't': (0xFB, 4), 'h': (0xBF, 4)})
snap = sys.argv[1]
def go(pokes, sched, frames, probe, every=10):
    sim = load(snap); tr = KeyTracer(); sim.set_tracer(tr)
    mem, reg, ops = sim.memory, sim.registers, sim.opcodes
    for a, v in pokes.items(): mem[a] = v
    fd, ia = sim.frame_duration, sim.int_active
    t = reg[25]; nxt = ((t+fd-ia)//fd)*fd; frame = 0; tr.pressed = set(sched(0)); out = []
    while frame < frames:
        pc = reg[24]; ops[mem[pc]]()
        t = reg[25]
        if t >= nxt:
            if t < nxt+ia:
                if reg[26] and sim.accept_interrupt(reg, mem, pc):
                    frame += 1; tr.pressed = set(sched(frame)); nxt += fd
                    if frame % every == 0: out.append((frame, probe(mem)))
            else: nxt += fd
    return out
nivel = lambda m: (m[0xD39A], m[0xD98B])
print('M con D079=255 (siguiente nivel):', go({0xD079: 255, 0xD39A: 5}, lambda f: {'m'} if 10 <= f < 20 else set(), 80, nivel, 20))
print('M sin trucos (D079=0, no hace nada):', go({0xD079: 0, 0xD39A: 5}, lambda f: {'m'} if 10 <= f < 20 else set(), 80, nivel, 20))
print('N con D079=255 (nivel anterior):', go({0xD079: 255, 0xD39A: 5}, lambda f: {'n'} if 10 <= f < 20 else set(), 80, nivel, 20))
print('H pausa: color de los atributos $5800 (frame, atributo, nivel):')
print(go({}, lambda f: {'h'} if 10 <= f < 20 else ({'h'} if 40 <= f < 50 else set()), 90, lambda m: (m[0x5800], m[0x5A00], m[0xD3A7]), 10))
print('T con D920=$05:', go({0xD920: 5}, lambda f: {'t'} if 10 <= f < 20 else set(), 60, lambda m: (m[0xD920], m[0xD921]), 10))

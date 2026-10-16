"""kempstontest.py - comprueba el joystick Kempston (lectura IN A,($1F) en $CD1D): bit0 derecha, bit1 izquierda, bit2 abajo, bit3 arriba, bit4 disparo (= tecla de bloque).
Se activa con D39E bit 0 (esquema de mandos del menu, tecla 5) y sólo afecta al jugador 1.
Uso: python3 -I kempstontest.py nivel2.sna"""
import sys; sys.path.insert(0, '/home/claude/tools')
from keytrace import *
def go(bits_por_frame, frames, probe):
    sim = load(sys.argv[1]); tr = KeyTracer(); sim.set_tracer(tr); tr.kemp = 0
    mem, reg, ops = sim.memory, sim.registers, sim.opcodes
    mem[0xD39E] |= 1; mem[0xD3BC] = 0
    fd, ia = sim.frame_duration, sim.int_active
    t = reg[25]; nxt = ((t+fd-ia)//fd)*fd; frame = 0; out = []
    while frame < frames:
        pc = reg[24]; ops[mem[pc]]()
        t = reg[25]
        if t >= nxt:
            if t < nxt+ia:
                if reg[26] and sim.accept_interrupt(reg, mem, pc):
                    frame += 1; nxt += fd; tr.kemp = bits_por_frame(frame)
                    if frame % 10 == 0: out.append((frame, probe(mem)))
            else: nxt += fd
    return out
pos = lambda m: (m[0xD3A7], m[0xD3A8], m[0xD98A])
for nom, bit in (('derecha', 1), ('izquierda', 2), ('abajo (agachar)', 4), ('arriba (saltar)', 8)):
    print(nom, go(lambda f, b=bit: b if 10 <= f < 40 else 0, 50, pos))
cnt = lambda m: sum(1 for i in range(140) if m[0xDE5A+i] in (0x45, 0x46, 0x47, 0x48))
print('disparo (bit4) mantenido 10 ciclos y soltado -> bloques en el mapa:', go(lambda f: 16 if 10 <= f < 24 else 0, 60, cnt)[-1])

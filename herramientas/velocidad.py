"""velocidad.py - mide cuantas interrupciones (frames de 50 Hz) dura un ciclo de juego ($D989 cambia en cada ciclo) en un nivel.
Uso: python3 -I velocidad.py nivel2.sna [frames]"""
import sys; sys.path.insert(0, '/home/claude/tools')
from keytrace import *
sim = load(sys.argv[1]); tr = KeyTracer(); sim.set_tracer(tr)
mem, reg, ops = sim.memory, sim.registers, sim.opcodes
N = int(sys.argv[2]) if len(sys.argv) > 2 else 400
fd, ia = sim.frame_duration, sim.int_active
t = reg[25]; nxt = ((t+fd-ia)//fd)*fd; frame = 0; last = mem[0xD989]; cambios = []
while frame < N:
    ops[mem[reg[24]]]()
    t = reg[25]
    if mem[0xD989] != last:
        last = mem[0xD989]; cambios.append(frame)
    if t >= nxt:
        if t < nxt+ia:
            if reg[26] and sim.accept_interrupt(reg, mem, reg[24]): frame += 1; nxt += fd
        else: nxt += fd
d = [b-a for a, b in zip(cambios, cambios[1:])]
print('frames entre ciclos:', d[:30])
print('media: %.2f frames/ciclo -> %.1f ciclos/s a 50 Hz (el Spectrum 48K genera 50.08 interrupciones/s)' % (sum(d)/len(d), 50.08/(sum(d)/len(d))))

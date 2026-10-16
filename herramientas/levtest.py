"""levtest.py - arranca un nivel concreto (1 jugador) y registra los enemigos de ciertos tipos.
Uso: python3 -I levtest.py tape/mundoN.sna mundo nivel_global tipos_hex(ej. 0c,f) frames paso"""
import sys; sys.path.insert(0, '/home/claude/tools')
from keytrace import *
snap, w, lv = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
tipos = [int(x, 16) for x in sys.argv[4].split(',')]; frames = int(sys.argv[5]); paso = int(sys.argv[6])
sim = load(snap); tr = KeyTracer(); sim.set_tracer(tr)
mem, reg, ops = sim.memory, sim.registers, sim.opcodes
fd, ia = sim.frame_duration, sim.int_active
t = reg[25]; nxt = ((t+fd-ia)//fd)*fd; frame = 0
sched = lambda f: {'1'} if 5 <= f < 12 else ({'r'} if 150 <= f < 156 else set())
tr.pressed = sched(0)
while frame < frames + 160:
    pc = reg[24]; ops[mem[pc]]()
    t = reg[25]
    if t >= nxt:
        if t < nxt+ia:
            if reg[26] and sim.accept_interrupt(reg, mem, pc):
                frame += 1; nxt += fd; tr.pressed = sched(frame)
                if frame == 140: mem[0xD39A] = lv; mem[0xD98B] = w; mem[0xD91D] = 1
                if frame > 170 and (frame-170) % paso == 0:
                    n = mem[0xD52C]
                    print(frame-170, 'lv', mem[0xD39A], [(k, mem[0xD3F8+22*k], mem[0xD3F9+22*k], mem[0xD3FA+22*k]) for k in range(n) if mem[0xD3F8+22*k+8] in tipos][:5], 'todos', [mem[0xD3F8+22*k+8] for k in range(n)], 'D98B', mem[0xD98B], 'D91D', mem[0xD91D], 'D3A7', mem[0xD3A7], mem[0xD3C4])
            else: nxt += fd

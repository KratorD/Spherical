"""menuseguir.py - pulsa cada tecla del menu (1-7) y DEJA CORRER el juego 500 frames para ver su efecto real (D91D jugadores, D39A nivel, D39B pantalla especial,
D39E esquema de mandos, F79B color de fondo claro/oscuro) y las rutinas por las que pasa. Con COVER=fichero registra la cobertura.
Uso: python3 -I menuseguir.py menu.sna"""
import sys; sys.path.insert(0, '/home/claude/tools')
import keytrace
from keytrace import *
keytrace.KEYS.update({'3': (0xF7, 2), '4': (0xF7, 3), '5': (0xF7, 4), '6': (0xEF, 4), '7': (0xEF, 3)})
def prueba(k, extra=()):
    sim = load(sys.argv[1]); tr = KeyTracer(); sim.set_tracer(tr)
    mem, reg, ops = sim.memory, sim.registers, sim.opcodes
    fd, ia = sim.frame_duration, sim.int_active
    t = reg[25]; nxt = ((t+fd-ia)//fd)*fd; frame = 0; rut = set()
    antes = (mem[0xD39E], mem[0xF79B])
    sched = lambda f: ({k} if 150 <= f < 215 else {'1'} if f == 400 else set())
    while frame < 700:
        pc = reg[24]; rut.add(pc)
        ops[mem[pc]]()
        t = reg[25]
        if t >= nxt:
            if t < nxt+ia:
                if reg[26] and sim.accept_interrupt(reg, mem, pc):
                    frame += 1; nxt += fd; tr.pressed = sched(frame)
                    if frame == 399: snap399 = (dict(D91D=mem[0xD91D], D39A=mem[0xD39A], D39B=hex(mem[0xD39B]), D39E=(antes[0], mem[0xD39E]), F79B=(antes[1], mem[0xF79B])), pc, bytes(mem[0xD109:0xD109+4]))
            else: nxt += fd
    return snap399, rut, dict(D91D=mem[0xD91D], D39A=mem[0xD39A], D39B=hex(mem[0xD39B]))
for k in '1234567':
    a, rut, fin = prueba(k)
    print(k, 'en el frame 399:', a[0], 'PC', hex(a[1]), '| tras pulsar 1 en el 400:', fin, '| pasa por $C8FB:', 0xC8FB in rut)

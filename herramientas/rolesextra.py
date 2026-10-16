"""rolesextra.py - completa el mapa de uso de sprites con lo que el barrido no ejerce: fotogramas de la maga (J2 = fotograma de J1 + $0D) y orbes
($3A normal, $3B poder doble). Se fuerza el fotograma del registro de J2 (+2 de $D3C4) y los bits de poder (+$15 bits 3-4 de J1 y J2), y se registra
qué fotograma sale realmente en pantalla. Uso: COVER=x ROLES=r.txt python3 -I rolesextra.py 2jugadores.sna"""
import sys; sys.path.insert(0, '/home/claude/tools')
from keytrace import *
sim = load(sys.argv[1]); tr = KeyTracer(); sim.set_tracer(tr)
mem, reg, ops = sim.memory, sim.registers, sim.opcodes
fd, ia = sim.frame_duration, sim.int_active
t = reg[25]; nxt = ((t+fd-ia)//fd)*fd; frame = 0; tr.pressed = {'2'}; n = 0
while frame < 900 and n < 60000000:
    ops[mem[reg[24]]](); n += 1
    t = reg[25]
    if t >= nxt:
        if t < nxt+ia and reg[26]: sim.accept_interrupt(reg, mem, reg[24])
        frame += 1; nxt += fd
        if frame == 12: tr.pressed = set()
        if frame == 140: mem[0xD39A] = 11; mem[0xD98B] = 1; mem[0xD91D] = 2
        if frame > 200:
            mem[0xD079] = 255
            mem[0xD3C6] = (frame // 3) % 13                         # fotograma 0..C de la maga
            mem[0xD3BC] = (mem[0xD3BC] & ~0x18) | (0x08 if (frame // 40) % 2 == 0 else 0x10)
            mem[0xD3D9] = (mem[0xD3D9] & ~0x18) | (0x10 if (frame // 40) % 2 == 0 else 0x08)
print('frames', frame, 'ops', n)

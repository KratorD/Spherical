"""pociontest2.py - efecto de la pocion (ENTER con D98C>0): mata a los enemigos de tipo 0-8 salvo el 4, borra las casillas peligrosas $41/$42 y reproduce la animacion de beber.
Uso: python3 -I pociontest2.py nivel2.sna"""
import sys; sys.path.insert(0, '/home/claude/tools')
from keytrace import *
sim = load(sys.argv[1]); tr = KeyTracer(); sim.set_tracer(tr)
mem, reg, ops = sim.memory, sim.registers, sim.opcodes
mem[0xD98C] = 2
mem[0xDE5A+60] = 0x41; mem[0xDE5A+61] = 0x42; mem[0xDE5A+62] = 0x43
mem[0xD52C] = 3                                   # 3 enemigos: tipo 0, tipo 4 (inmune) y tipo 9 (inmune)
for k, tipo in enumerate((0, 4, 9)):
    b = 0xD3F8 + 22*k; mem[b] = 60 + 10*k; mem[b+1] = 100; mem[b+2] = 0x24; mem[b+8] = tipo; mem[b+7] = 1
fd, ia = sim.frame_duration, sim.int_active
t = reg[25]; nxt = ((t+fd-ia)//fd)*fd; frame = 0
while frame < 120:
    pc = reg[24]; ops[mem[pc]]()
    t = reg[25]
    if t >= nxt:
        if t < nxt+ia:
            if reg[26] and sim.accept_interrupt(reg, mem, pc):
                frame += 1; nxt += fd; tr.pressed = {'ENTER'} if 10 <= frame < 20 else set()
        else: nxt += fd
print('pociones restantes (D98C):', mem[0xD98C], '(2 -> 1)')
print('enemigos x tras la pocion (FF = eliminado):', [mem[0xD3F8+22*k] for k in range(3)], 'tipos', [0, 4, 9])
print('casillas $41,$42 (borradas), $43 (se conserva):', [mem[0xDE5A+60], mem[0xDE5A+61], mem[0xDE5A+62]])

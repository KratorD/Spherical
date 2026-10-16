"""modtest.py - comprueba recetas de modificación parcheando la memoria del snapshot del menú y arrancando una partida con la tecla 1.
Receta 1: vidas iniciales ($AAA6, operando de LD A,$04). Receta 2: energía inicial ($AAAB, operando de LD A,$64). Receta 3: daño por contacto ($AB1B, operando de LD C,$FF) = -3.
Uso: python3 -I modtest.py menu.sna"""
import sys; sys.path.insert(0, '/home/claude/tools')
from keytrace import *
def jugar(snap, pokes, frames=420, mover=False):
    sim = load(snap); tr = KeyTracer(); sim.set_tracer(tr); mem, reg, ops = sim.memory, sim.registers, sim.opcodes
    for a, v in pokes.items(): mem[a] = v
    fd, ia = sim.frame_duration, sim.int_active
    t = reg[25]; nxt = ((t+fd-ia)//fd)*fd; f = 0; tr.pressed = set(); hist = []
    while f < frames:
        ops[mem[reg[24]]]()
        t = reg[25]
        if t >= nxt:
            if t < nxt+ia:
                if reg[26] and sim.accept_interrupt(reg, mem, reg[24]):
                    f += 1; nxt += fd; tr.pressed = {'1'} if 150 <= f < 260 else set(); hist.append(mem[0xD3EF])
            else: nxt += fd
    return mem[0xD2E8], mem[0xD3EF], hist
for nombre, pk in (('sin parche', {}), ('vidas iniciales = 2 ($AAA6)', {0xAAA6: 2}), ('vidas iniciales = 3', {0xAAA6: 3}), ('energía inicial = 50 ($AAAB)', {0xAAAB: 50}), ('vidas iniciales = 5 (MAL: desborda el marcador)', {0xAAA6: 5})):
    print('%-48s vidas, energía = %s' % (nombre, jugar(sys.argv[1], pk)[:2]))

# ---- Receta 4: limitador de velocidad. El juego no sincroniza con la interrupcion; se inserta una espera (CALL $CCB2 = EI+HALT) por ciclo
# mediante un trampolin en los bytes libres $F7BC-$F7FF (dentro del bloque de cinta). AB78 (9 bytes) = JP $F7C0 + 6 NOP; en $F7C0 va la espera y la rutina original.
def trampolin(n_esperas):
    p = {}
    orig = [0x3A, 0x89, 0xD9, 0x3C, 0xE6, 0x03, 0x32, 0x89, 0xD9]          # LD A,($D989) / INC A / AND 3 / LD ($D989),A
    for a, b in zip(range(0xAB78, 0xAB81), [0xC3, 0xC0, 0xF7] + [0] * 6): p[a] = b
    code = [0xCD, 0xB2, 0xCC] * n_esperas + orig + [0xC3, 0x81, 0xAB]      # esperas + original + JP $AB81
    for i, b in enumerate(code): p[0xF7C0 + i] = b
    return p
def ciclos_por_segundo(snap, pokes, frames=900):
    sim = load(snap); tr = KeyTracer(); sim.set_tracer(tr); mem, reg, ops = sim.memory, sim.registers, sim.opcodes
    for a, v in pokes.items(): mem[a] = v
    fd, ia = sim.frame_duration, sim.int_active
    t = reg[25]; nxt = ((t+fd-ia)//fd)*fd; f = 0; tr.pressed = set(); n0 = None; n = 0; f0 = None
    while f < frames:
        pc = reg[24]
        if pc == 0xAB81:
            n += 1
        ops[mem[pc]]()
        t = reg[25]
        if t >= nxt:
            if t < nxt+ia:
                if reg[26] and sim.accept_interrupt(reg, mem, pc):
                    f += 1; nxt += fd; tr.pressed = {'1'} if 150 <= f < 260 else set()
                    if f == 400: n = 0; f0 = f
            else: nxt += fd
    return n * 50.0 / (frames - f0)
print('ciclos/s sin parche      :', round(ciclos_por_segundo(sys.argv[1], {}), 1))
print('con 1 espera por ciclo   :', round(ciclos_por_segundo(sys.argv[1], trampolin(1)), 1))
print('con 2 esperas por ciclo  :', round(ciclos_por_segundo(sys.argv[1], trampolin(2)), 1))

# ---- Recetas 5 y 6: duración del escudo ($B44A, operando de LD (IY+$18),$96) y del poder del orbe ($B4DD, operando de LD (IY+$19),$C0): se llama a $B38D con la casilla bajo el jugador
def recoge(snap, casilla, pokes):
    sim = load(snap); tr = KeyTracer(); sim.set_tracer(tr); mem, reg, ops = sim.memory, sim.registers, sim.opcodes
    for a, v in pokes.items(): mem[a] = v
    for i in range(140): mem[0xDE5A+i] = 0
    mem[0xD3A7] = 24; mem[0xD3A8] = 0x40; mem[0xD3BC] = 0
    mem[0xDE5A + (0x40 >> 4)*14 + 24//8] = casilla
    reg[10] = 0xD3; reg[11] = 0xA7; reg[24] = 0xB38D; reg[12] = 0xFFEE; mem[0xFFEE] = 0xF0; mem[0xFFEF] = 0xFF; n = 0
    while reg[24] != 0xFFF0 and n < 20000: ops[mem[reg[24]]](); n += 1
    return mem[0xD3BF], mem[0xD3C0]
print('escudo ($38): +$18 =', hex(recoge(sys.argv[1], 0x38, {})[0]), '| con $B44A=$FF:', hex(recoge(sys.argv[1], 0x38, {0xB44A: 0xFF})[0]))
print('orbe ($33): +$19 =', hex(recoge(sys.argv[1], 0x33, {})[1]), '| con $B4DD=$FF:', hex(recoge(sys.argv[1], 0x33, {0xB4DD: 0xFF})[1]))

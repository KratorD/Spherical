"""niveltest.py - verifica el paso de nivel $C524 -> carga de nivel $C563 -> carga de mundo $CFB3, incl. el intercambio de casillas del nivel 70.
La carga de cinta (ROM LD-BYTES, que el simulador no tiene) se sustituye en $D01F por una rutina que copia el bloque de tape/<4+w>_<w>.bin.
Uso: python3 -I niveltest.py dir_cinta(tape/)"""
import sys, os; sys.path.insert(0, '/home/claude/tools')
from keytrace import *
tape = sys.argv[1]
def bloque(w): return open(os.path.join(tape, '%d_%d.bin' % (4+w, w)), 'rb').read()
def escenario(nombre, nivel, sel=0, modo=1, frames=500, seguir=False, puntos=None, puntos2=None):
    w0 = nivel // 10
    sim = load(os.path.join(tape, 'mundo%d.sna' % w0)); tr = KeyTracer(); sim.set_tracer(tr)
    mem, reg, ops = sim.memory, sim.registers, sim.opcodes
    if os.environ.get('KEMP'): tr.kemp = 0; mem[0xD39E] |= 1      # joystick Kempston activo (cubre las esperas de disparo con joystick)
    if puntos is not None: mem[0xD3BD] = puntos & 255; mem[0xD3BE] = puntos >> 8
    if puntos2 is not None: mem[0xD3DA] = puntos2 & 255; mem[0xD3DB] = puntos2 >> 8
    mem[0xD39A] = nivel; mem[0xD98B] = w0; mem[0xD91D] = modo; mem[0xD39B] = sel; mem[0xD079] = 255
    if w0 == 7 and nivel >= 70:            # en el mundo 7 el juego ya hizo el intercambio de casillas al entrar en el nivel 70
        pass
    reg[24] = 0xC524; reg[12] = 0xFFFC; mem[0xFFFC] = 0xF0; mem[0xFFFD] = 0xFF
    cargas = []; orig = None; fd, ia = sim.frame_duration, sim.int_active
    t = reg[25]; nxt = ((t+fd-ia)//fd)*fd; frame = 0; ad45 = False; nops = 0
    while frame < frames and nops < 40000000:
        pc = reg[24]
        if pc == 0xD01F:                                   # LD-BYTES simulado
            a = reg[0]; ix = reg[8] << 8 | reg[9]; de = reg[4] << 8 | reg[5]
            if a == 0:                                     # cabecera: nombre = '0'+mundo pedido
                need = mem[0xD98B]; cargas.append(need)
                for k in range(17): mem[ix+k] = 0
                mem[ix] = 3; mem[ix+1] = 0x30 + need
                for k in range(1, 10): mem[ix+1+k] = 0x20
            else:                                          # datos
                b = bloque(mem[0xD98B])
                for k in range(de): mem[ix+k] = b[k+1] if len(b) > de else b[k]
            sp = reg[12]; reg[24] = mem[sp] | mem[sp+1] << 8; reg[12] = (sp+2) & 0xFFFF
            reg[1] = 0x01                                  # C=1 (carga correcta), Z=0
            continue
        if pc == 0xC5D0 and orig is None: orig = bytes(mem[0x9E60:0x9E60+0x2D0])
        if pc == 0xAD45:
            ad45 = True
            if not seguir: break
        ops[mem[pc]](); nops += 1
        t = reg[25]
        if t >= nxt:
            if t < nxt+ia and reg[26]: sim.accept_interrupt(reg, mem, pc)
            frame += 1; nxt += fd
            if os.environ.get('KEMP'): tr.kemp = 16 if frame % 40 < 6 else 0
            tr.pressed = ({'SPACE'} if frame % 40 < 6 else {'ENTER'} if frame % 40 in range(20, 26) else {'s'} if frame % 40 in range(30, 34) else set())
    ok_swap = None
    if mem[0xD39A] == 70:
        ok_swap = all(bytes(mem[0x9E60+36*i:0x9E60+36*i+32]) == bytes(mem[0x6F00+36*i:0x6F00+36*i+32]) and set(mem[0x9E60+36*i+32:0x9E60+36*i+36]) == {mem[0xF79B]} for i in range(20))
    print('%-34s nivel %2d sel %02X -> D39A=%2d D98B=%d D39B=%02X cargas de cinta=%s fin=%s%s' % (nombre, nivel, sel, mem[0xD39A], mem[0xD98B], mem[0xD39B], cargas, ad45,
          '' if ok_swap is None else ' | casillas 18h-2Bh intercambiadas (bitmaps 9E60 == 6F00, atributos = F79B): %s' % ok_swap))
    return sim, orig
for nom, niv, sel in (('nivel normal dentro del mundo', 3, 0), ('cambio de mundo 0->1', 9, 0), ('9->10 (jefe del mundo 1)', 9, 0),
                      ('entrada al nivel 70 (intercambio)', 69, 0), ('salida del nivel 70 (restaura)', 70, 0),
                      ('78 salta el 79 -> 80', 78, 0), ('80 -> 81 = fin del juego', 80, 0), ('tras la copa ($57): avanza 2', 20, 0x57), ('desde sala de bonus ($42)', 20, 0x42)):
    escenario(nom, niv, sel)
# secuencia completa 69 -> 70 -> 71: al salir del nivel 70 las casillas 18h-2Bh vuelven a ser las originales
sim, orig = escenario('entrada al 70 (para la secuencia)', 69)
mem, reg = sim.memory, sim.registers
mem[0xD39A] = 70; reg[24] = 0xC524; reg[12] = 0xFFFC; mem[0xFFFC] = 0xF0; mem[0xFFFD] = 0xFF
for _ in range(3000000):
    if reg[24] == 0xAAC7: break
    sim.opcodes[mem[reg[24]]]()
print('al salir del 70: D39A =', mem[0xD39A], '| casillas originales restauradas (9E60 == copia previa):', bytes(mem[0x9E60:0x9E60+0x2D0]) == orig)
if len(sys.argv) > 2 and sys.argv[2] == 'final':     # tras el fin del juego: recorre la pantalla final, la entrada de nombre y la tabla de puntuaciones
    escenario('fin del juego con puntuacion alta', 80, 0, 1, 6000, True, 6000)
    escenario('fin del juego, 2 jugadores', 80, 0, 2, 9000, True, 6000, 7000)

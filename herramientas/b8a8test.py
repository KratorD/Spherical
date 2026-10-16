"""b8a8test.py - ejecuta DIRECTAMENTE la única instrucción de $B8A8 (JP $BE70) con el PC forzado, para completar la cobertura de ejecución.
Es una ejecución forzada: ningún valor de tipo de enemigo llega ahí (despachotest.py). Uso: python3 -I b8a8test.py nivel2.sna"""
import sys; sys.path.insert(0, '/home/claude/tools')
from keytrace import *
sim = load(sys.argv[1]); tr = KeyTracer(); sim.set_tracer(tr); mem, reg, ops = sim.memory, sim.registers, sim.opcodes
reg[24] = 0xB8A8; ops[mem[reg[24]]]()
print('tras ejecutar $B8A8: PC = $%04X (esperado $BE70)' % reg[24])

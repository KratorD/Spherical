import sys; sys.path.insert(0,'/home/claude/tools')
from keytrace import *
sim=load('menu.sna'); mem,reg,ops=sim.memory,sim.registers,sim.opcodes
for i,v in enumerate((5000,3000,1000,500,100)): mem[0xD109+15*i]=v&255; mem[0xD10A+15*i]=v>>8
reg[24]=0xADAC; reg[12]=0xFFFC; mem[0xFFFC]=0xF0; mem[0xFFFD]=0xFF; reg[6]=0; reg[7]=10   # HL=10
n=0
while reg[24]!=0xFFF0 and n<200000: ops[mem[reg[24]]](); n+=1
print('puntuacion 10 no entra en la tabla; vuelve a FFF0:', reg[24]==0xFFF0, [(mem[0xD109+15*i]|mem[0xD10A+15*i]<<8) for i in range(5)])

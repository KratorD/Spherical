import sys; sys.path.insert(0,'/home/claude/tools')
from keytrace import *
def run(path,pokes,frames,probe,every=2):
    sim=load(path); tr=KeyTracer(); sim.set_tracer(tr)
    mem,reg,ops=sim.memory,sim.registers,sim.opcodes
    for a,v in pokes.items(): mem[a]=v
    fd,ia=sim.frame_duration,sim.int_active
    t=reg[25]; nxt=((t+fd-ia)//fd)*fd; frame=0; out=[]
    while frame<frames:
        pc=reg[24]; ops[mem[pc]]()
        t=reg[25]
        if t>=nxt:
            if t<nxt+ia:
                if reg[26] and sim.accept_interrupt(reg,mem,pc):
                    frame+=1; nxt+=fd
                    if frame%every==0: out.append(probe(mem))
            else: nxt+=fd
    return out
def rec(tipo,**k):
    p={0xD52C:1}
    base=0xD3F8
    p[base+0]=k.get('x',0x30);p[base+1]=k.get('y',0x40);p[base+2]=k.get('f',0x24)
    p[base+7]=k.get('d',1)&0xFF;p[base+8]=tipo
    for i,n in ((9,'a'),(10,'b'),(11,'c'),(12,'e'),(13,'g')):
        if n in k: p[base+i]=k[n]
    return p
pr=lambda mem:tuple(mem[0xD3F8+i] for i in (0,1,2,7,9,10,13))
tests={
 4:rec(4,x=0x30,y=0x20,f=0x46,b=0x20),
 5:rec(5,x=0x10,y=0x40,f=0x3D,d=0,a=0),
 6:rec(6,x=0x60,y=0x40,f=0x3D,d=0,a=0),
 7:rec(7,x=0x30,y=0x40,f=0x47,d=1,a=0),
 8:rec(8,x=0x30,y=0x40,f=0x4A,d=1,a=0xF5,b=0xD9),
 0xA:rec(0xA,x=0x60,y=0x40,f=0x4F,d=0,a=0,b=0x40,c=0x60),
 0xB:rec(0xB,x=0x02,y=0x90,f=0x4D,d=1,a=0),
 9:rec(9,x=0x60,y=0x40,f=0x48,d=3,b=0x40,c=0x60),
 0xD:rec(0xD,x=0x40,y=0x40,f=0x48,d=0,b=0x40,c=0x40),
 0xE:rec(0xE,x=0x60,y=0x20,f=0x48,d=0,b=0x20,c=0x60),
 2:rec(2,x=0x30,y=0x40,f=0x30,d=1,a=0x9B,b=0xD9),
 0:rec(0,x=0x20,y=0x90,f=0x24,d=1),
 1:rec(1,x=0x20,y=0x10,f=0x28,d=1),
}
which=[int(a,16) for a in sys.argv[1:]] or list(tests)
for t in which:
    print('--- tipo %X (x,y,frame,+7,+9,+A,+D)'%t)
    r=run('/home/claude/work/nivel2.sna',tests[t],70,pr,every=3)
    print(r[:24])

import sys; sys.path.insert(0,'/home/claude/tools')
from keytrace import KeyTracer, load
from collections import defaultdict
class LogMem(list):
    log=None; pc=0
    def __setitem__(self,i,v):
        if isinstance(i,int) and LogMem.log is not None: LogMem.log.append((i,v))
        list.__setitem__(self,i,v)
def run(path, sched, frames, record_from=0):
    sim=load(path)
    mem0=sim.memory
    lm=LogMem(mem0); sim.memory=lm
    # opcodes capturaron la lista original: recrear
    sim.create_opcodes()
    tr=KeyTracer(); sim.set_tracer(tr)
    reg,ops=sim.registers,sim.opcodes
    fd,ia=sim.frame_duration,sim.int_active
    next_int=((reg[25]+fd-ia)//fd)*fd; frame=0; tr.pressed=set(sched(0))
    out=[]
    while frame<frames:
        pc=reg[24]
        LogMem.log=[] if frame>=record_from else None
        ops[lm[pc]]()
        if LogMem.log: out+= [(frame,pc,a,v) for a,v in LogMem.log]
        t=reg[25]
        if t>=next_int:
            if t<next_int+ia:
                if reg[26] and sim.accept_interrupt(reg,lm,pc):
                    frame+=1; tr.pressed=set(sched(frame)); next_int+=fd
            else: next_int+=fd
    return out,sim
if __name__=='__main__':
    snap=sys.argv[1]
    out,sim=run('/home/claude/work/%s.sna'%snap, lambda f:{'SPACE'} if (f%20)<2 else set(), 60)
    by=defaultdict(list)
    for fr,pc,a,v in out:
        if a<0x5B00 or 0xF200<=a: continue
        by[a].append((fr,pc,v))
    print(len(out),'escrituras;',len(by),'direcciones')
    for a in sorted(by):
        l=by[a]
        if len(l)<=6: print('%04X'%a,[(fr,'%04X'%pc,'%02X'%v) for fr,pc,v in l])

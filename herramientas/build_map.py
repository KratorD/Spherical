import sys, random
sys.path.insert(0,'/home/claude/tools')
from keytrace import run
W='/home/claude/work/'
allx=set()
random.seed(7)
keys=['q','a','o','p','SPACE','ENTER','r','h']
for snap in ('menu','nivel2','nivel4'):
    for sch in [lambda f:set()]+[ (lambda f,k=k:{k}) for k in keys]+[(lambda f,k=k:{k} if f%12<2 else set()) for k in keys]:
        try:
            ex,_,_=run(W+snap+'.sna',sch,400); allx|=ex
        except Exception as e: print('err',snap,e)
    # fuzz: combinaciones aleatorias que cambian cada 6-20 frames
    for seed in range(12):
        rnd=random.Random(seed*31+len(snap)); cur=set(); nxt=0
        def sch(f):
            global cur,nxt
            if f>=nxt:
                cur={k for k in keys if k not in('r','h') and rnd.random()<0.3}
                if rnd.random()<0.05: cur.add('r')
                nxt=f+rnd.randint(6,20)
            return cur
        try:
            ex,_,_=run(W+snap+'.sna',sch,1500); allx|=ex
        except Exception as e: print('err fuzz',snap,e)
    print(snap,len(allx))
open(W+'combined2.map','w').write(''.join('$%04X\n'%a for a in sorted(allx) if a>=0x4000))

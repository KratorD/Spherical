import sys
from PIL import Image, ImageDraw
sys.argv=[sys.argv[0]]+sys.argv[1:]
snap=sys.argv[1]; out=sys.argv[2]
d=open(snap,'rb').read()[27:]
m=lambda a,n=1:d[a-0x4000:a-0x4000+n]
PAL=[(0,0,0),(0,0,205),(205,0,0),(205,0,205),(0,205,0),(0,205,205),(205,205,0),(205,205,205)]
def col(c,br): 
    f=1.2 if br else 1.0
    return tuple(min(255,int(v*f)) for v in c)
S=3
def mk(n,cols,getter,fn):
    rows=(n+cols-1)//cols
    W=16*S+6; Hh=16*S+16
    im=Image.new('RGB',(cols*W,rows*Hh),(30,30,30)); dr=ImageDraw.Draw(im)
    for i in range(n):
        t=getter(i); ox=(i%cols)*W+3; oy=(i//cols)*Hh+12
        im.paste(t.resize((16*S,16*S),Image.NEAREST),(ox,oy))
        dr.text((ox,oy-11),'%02X'%i,fill=(255,255,0))
    im.save(fn)
def tile(c):
    base=0x9B00+36*c; bm=m(base,32); at=m(base+32,4); im=Image.new('RGB',(16,16))
    for y in range(16):
        for x in range(16):
            bit=(bm[y*2+x//8]>>(7-x%8))&1; a=at[(y//8)*2+x//8]
            im.putpixel((x,y),col(PAL[(a&7) if bit else (a>>3)&7],(a>>6)&1))
    return im
def spr(f):
    base=0x6100+32*f; bm=m(base,32); im=Image.new('RGB',(16,16))
    for y in range(16):
        for x in range(16):
            bit=(bm[y*2+x//8]>>(7-x%8))&1
            im.putpixel((x,y),(255,255,255) if bit else (0,0,60))
    return im
mk(0x5B,12,tile,out+'/atlas_casillas.png')
mk(0x70,14,spr,out+'/atlas_sprites.png')

import re
L=open('/home/claude/work/spherical_anotado.skool',encoding='utf-8').read().split('\n')
ents=[];cur=[]
for l in L:
    if l.strip()=='' :
        if cur: ents.append(cur);cur=[]
    else: cur.append(l)
if cur: ents.append(cur)
mac=lambda s:re.sub(r'#R(\$[0-9A-Fa-f]{4})',r'\1',s)
out=['# Spherical (ZX Spectrum 48K) — Código fuente comentado (desensamblado anotado)\n',
'> **Uso personal, educativo y de preservación.** Este fichero deriva del código de *Spherical* (© Rainbow Arts / Electronic Zoo, 1989) y contiene sus instrucciones originales. **No lo publiques ni lo redistribuyas.** Si quieres compartir algo, comparte `Spherical_ZX_Spectrum_Analisis_Completo.md`, que solo contiene descripciones.\n',
'> Procedencia: generado desde `spherical_anotado.skool` (SkoolKit 10.1), que reensambla idéntico byte a byte a la RAM `$5B00-$FFFF`. Los comentarios son del análisis; los marcados **V** en el documento de análisis se comprobaron ejecutando el juego.\n',
'> **Qué incluye y qué no.** Todo el **código** (rutinas completas, con sus comentarios) y las tablas pequeñas. Los bloques de datos grandes (gráficos, mapas, tablas de sonido, restos del cargador) se resumen con su dirección, tamaño y descripción, mostrando solo las primeras líneas: son *assets*, no lógica. El volcado completo está en el `.skool`.\n',
'Cómo leerlo: cada bloque empieza con su dirección y un comentario de qué hace; dentro, `; …` explica instrucciones o tramos. `*` delante de una dirección = destino de salto. Convenciones y mapa de memoria: ver el documento de análisis (§4, §7).\n','---\n']
nc=0;nd=0;ns=0
for e in ents:
    head=[x for x in e if x.startswith(';')]
    # leading comment block vs body
    i=0
    while i<len(e) and (e[i].startswith(';') or e[i].startswith('@')): i+=1
    pre=e[:i]; body=e[i:]
    if not body: continue
    m=re.match(r'^([a-z ])?[*]?\$([0-9A-F]{4})',body[0])
    if not m: continue
    kind=body[0][0] if body[0][0] in 'bcstuw' else 'c'
    addr=re.match(r'^.?[*]?\$([0-9A-F]{4})',body[0]).group(1)
    last=re.match(r'^.?[*]?\$([0-9A-F]{4})',body[-1])
    labels=[x[7:] for x in pre if x.startswith('@label=')]
    ptxt=[mac(x[2:] if x.startswith('; ') else x[1:]) for x in pre if x.startswith(';')]
    title=ptxt[0] if ptxt and ptxt[0] else 'Bloque'
    desc='\n'.join(ptxt[1:]).strip('\n') if len(ptxt)>1 else ''
    tipo={'c':'Código','b':'Datos','t':'Texto','s':'Espacio','u':'Sin usar','w':'Datos (palabras)'}.get(kind,'Código')
    out.append('## `$%s` — %s\n'%(addr,title.rstrip('.')))
    out.append('*%s%s*\n'%(tipo,(' · etiqueta `%s`'%labels[0]) if labels else ''))
    if desc: out.append(desc+'\n')
    if kind=='c': nc+=1
    else: nd+=1
    lines=[mac(x) for x in body]
    if kind in 'bsuw' and len(lines)>8:
        a0=int(addr,16); a1=int(last.group(1),16) if last else a0
        ns+=1
        out.append('```asm\n'+'\n'.join(lines[:4])+'\n; … (%d líneas de datos omitidas; bloque $%s-$%s, ≈%d bytes; ver .skool)\n```\n'%(len(lines)-4,addr,'%04X'%a1,a1-a0+16))
    else:
        out.append('```asm\n'+'\n'.join(lines)+'\n```\n')
open('/home/claude/work/Spherical_ZX_Spectrum_Codigo_Comentado.md','w',encoding='utf-8').write('\n'.join(out))
print(len(ents),nc,nd,ns)

"""
MT1 (1 fita) e MT2 (2 fitas) da Turing Airlines. 
Fita infinita à direita: célula 0 = '>' (marcador de início, intransponível). ' ' = branco.
'$' = separador entrada|zona (rodada 1); '%' = o mesmo, na rodada 2.
"""
B, S = ' ', '>'
SYM = ['L','O','l','o','p','1','#','|','m']

def K(c): return ('K', c % 24)
def V(c): return ('V', c % 24)
def W(c): return ('W', c % 24)

def build_mt1():
    d = {}
    def add(q, a, q2, b, m):
        assert (q, a) not in d, f"Conflito em {(q, a)}"
        d[(q, a)] = (q2, b, m)
        
    add('i0', S, 'i1', S, +1)
    add('i1','L','i1','O',+1); add('i1','O','i1','L',+1); add('i1','#','i2','#',+1)
    add('i2','L','i2','L',+1); add('i2','O','i2','O',+1); add('i2','#','i3','#',+1)
    add('i3','L','i3','l',+1); add('i3','O','i3','o',+1); add('i3','#','i4','#',+1)
    
    for x in ['p','1','#','|']: add('i4', x, 'i4', x, +1)
    add('i4', B, 'i5', '$', -1)
    for x in ['L','O','l','o','p','1','#','|']: add('i5', x, 'i5', x, -1)
    add('i5', S, K(0), S, +1)

    for c in range(24):
        q = K(c)
        add(q,'L',K(c+1),'L',+1); add(q,'O',K(c-1),'O',+1)
        add(q,'l',q,'l',+1); add(q,'o',q,'o',+1); add(q,'#',q,'#',+1)
        add(q,'p',K(c+1),'p',+1); add(q,'m',q,'m',+1)
        add(q,'|',V(c),'m',+1) # fim da rodada 1
        add(q,'%',V(c),'%',+1) # fim da rodada 2
        if c < 23: add(q,'1',K(c+1),'1',+1)
        else:      add(q,'1','T1','r',+1)

    for x in SYM+['$','%']: add('T1', x, 'T1', x, +1); add('T2', x, 'T2', x, -1)
    add('T1', B, 'T2', '1', -1); add('T2', 'r', K(0), '1', +1)

    for c in range(24):
        for x in ['L','O','l','o','p','1','#','m','$','%']: add(V(c), x, V(c), x, +1)
        add(V(c), B, W(c), '#', +1)
        if c >= 1: add(W(c), B, W(c-1), '1', +1)
        else:      add(W(0), B, 'Ret', '#', -1)

    add('Ret','1','Ret','1',-1); add('Ret','#','Ret','#',-1)
    add('Ret','$','j1','%',-1); add('Ret','%','Fa',B,-1)

    for x in ['L','O','l','o','p','1','#','m']: add('j1', x, 'j1', x, -1); add('Fa', x, 'Fa', B, -1)
    add('j1', S, 'j2', S, +1); add('Fa', S, 'halt', S, +1)

    for x in ['L','O']: add('j2', x, 'j2', x, +1)
    add('j2','#','j3','#',+1)
    add('j3','L','j3','l',+1); add('j3','O','j3','o',+1); add('j3','#','j4','#',+1)
    add('j4','l','j4','L',+1); add('j4','o','j4','O',+1); add('j4','#','j5','#',-1)
    
    for x in ['L','O','l','o','#']: add('j5', x, 'j5', x, -1)
    add('j5', S, K(0), S, +1)
    
    return d

def build_mt2():
    d = {}
    def add(q, a, q2, b, m, w2=B, m2=0, a2=B):
        k = (q, a, a2)
        assert k not in d, k
        d[k] = (q2, b, w2, m, m2)
        
    add('i0', S, 'i1', S, +1, S, +1, S)
    add('i1','L','i1','O',+1); add('i1','O','i1','L',+1); add('i1','#','i2','#',+1)
    add('i2','L','i2','L',+1); add('i2','O','i2','O',+1); add('i2','#','i3','#',+1)
    add('i3','L','i3','l',+1); add('i3','O','i3','o',+1); add('i3','#','j5','#',-1)

    for c in range(24):
        q = K(c)
        add(q,'L',K(c+1),'L',+1); add(q,'O',K(c-1),'O',+1)
        add(q,'l',q,'l',+1); add(q,'o',q,'o',+1); add(q,'#',q,'#',+1)
        add(q,'p',K(c+1),'p',+1); add(q,'m',q,'m',+1)
        if c < 23: add(q,'1',K(c+1),'1',+1)
        else:      add(q,'1',K(0),'1',+1,'1',+1) # dia virou: escreve na fita 2
        add(q,'|',W(c),'m',0,'#',+1) # fim da rodada 1
        add(q,B,W(c),B,0,'#',+1) # fim da rodada 2

    for c in range(24):
        for a in ['m',B]:
            if c >= 1: add(W(c),a,W(c-1),a,0,'1',+1)
    add(W(0),'m','j1','m',-1,'#',+1)
    add(W(0),B,'halt',B,0,'#',+1)

    for x in ['L','O','l','o','p','1','#','m']: add('j1', x, 'j1', x, -1)
    add('j1', S, 'j2', S, +1)
    for x in ['L','O']: add('j2', x, 'j2', x, +1)
    add('j2','#','j3','#',+1)
    add('j3','L','j3','l',+1); add('j3','O','j3','o',+1); add('j3','#','j4','#',+1)
    add('j4','l','j4','L',+1); add('j4','o','j4','O',+1); add('j4','#','j5','#',-1)
    
    for x in ['L','O','l','o','#']: add('j5', x, 'j5', x, -1)
    add('j5', S, K(0), S, +1)
    
    return d

def run1(d, word, trace=False):
    t = {0: S}; t.update({i+1: ch for i, ch in enumerate(word)})
    h, q, n, tr = 0, 'i0', 0, []
    if trace: tr.append((0, q, dict(t), h))
    while q != 'halt':
        q, b, m = d[(q, t.get(h, B))]
        if h == 0: assert b == S and m == +1
        if b == B: t.pop(h, None)
        else: t[h] = b
        h += m; n += 1; assert h >= 0
        if trace: tr.append((n, q, dict(t), h))
    return t, h, n, tr

def run2(d, word, trace=False):
    t1 = {0: S}; t1.update({i+1: ch for i, ch in enumerate(word)}); t2 = {0: S}
    h1 = h2 = 0; q = 'i0'; n = 0; tr = []
    if trace: tr.append((0, q, dict(t1), h1, dict(t2), h2))
    while q != 'halt':
        q, b1, b2, m1, m2 = d[(q, t1.get(h1, B), t2.get(h2, B))]
        if h1 == 0: assert b1 == S and m1 == +1
        if h2 == 0: assert b2 == S and m2 == +1
        for t, h, b in ((t1, h1, b1), (t2, h2, b2)):
            if b == B: t.pop(h, None)
            else: t[h] = b
        h1 += m1; h2 += m2; n += 1; assert h1 >= 0 and h2 >= 0
        if trace: tr.append((n, q, dict(t1), h1, dict(t2), h2))
    return t1, t2, h1, h2, n, tr

def lon(deg): return ('L' if deg >= 0 else 'O') * (abs(deg)//15)
def enc(o,hub,dst,h0,d1,w,d2): return lon(o)+'#'+lon(hub)+'#'+lon(dst)+'#'+'p'*h0+'#'+'1'*d1+'|'+'1'*w+'#'+'1'*d2
def off(g): return g//15 if g >= 0 else -((-g)//15)
def ref(o,hub,dst,h0,d1,w,d2):
    sA = (h0-off(o)+off(hub)) % 24; sB = (h0-off(o)+off(dst)) % 24
    A = divmod(sA+d1, 24); Bv = divmod(sB+d1+w+d2, 24)
    return (A[1],A[0]), (Bv[1],Bv[0]) # (hora, dias)

def expected(*a):
    (hA,qA),(hB,qB) = ref(*a)
    return '1'*qA+'#'+'1'*hA+'#'+'1'*qB+'#'+'1'*hB+'#'

def block(t): # unico bloco nao branco apos '>'
    cells = sorted(i for i in t if i > 0)
    if not cells: return ''
    assert cells == list(range(cells[0], cells[-1]+1)), 'bloco nao contiguo'
    return ''.join(t[i] for i in cells)

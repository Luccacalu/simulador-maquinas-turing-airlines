# -*- coding: utf-8 -*-
import random, itertools
from tm import *

print("Construindo maquinas...")
d1m, d2m = build_mt1(), build_mt2()

def chk(e):
    w = enc(*e)
    x = expected(*e)
    t, h, n1, _ = run1(d1m, w)
    t1, t2, _, _, n2, _ = run2(d2m, w)
    return block(t) == x and h == 1 and block(t2) == x, n1, n2

if __name__ == "__main__":
    ex1 = (-75, 15, 15, 15, 4, 0, 0)
    ex2 = (-45, 0, 135, 22, 11, 3, 12)
    
    print("\n[Testando Exemplo 1 - Voo Direto]")
    print(f"Entrada: {ex1}")
    print(f"Fita codificada: {enc(*ex1)}")
    print(f"Saída Referência: {ref(*ex1)}")
    res1 = chk(ex1)
    print(f"MTs Corretas?: {res1[0]} | Passos MT1: {res1[1]} | Passos MT2: {res1[2]}")

    print("\n[Testando Exemplo 2 - Com Conexao]")
    print(f"Entrada: {ex2}")
    print(f"Fita codificada: {enc(*ex2)}")
    print(f"Saída Referência: {ref(*ex2)}")
    res2 = chk(ex2)
    print(f"MTs Corretas?: {res2[0]} | Passos MT1: {res2[1]} | Passos MT2: {res2[2]}")

    print("\n[Rodando bateria de testes massivos...]")
    rng = random.Random(1)
    lons = [15*k for k in range(-12, 13)]
    
    # Teste 1: 15.625 entradas (todas combinacoes de longitudes)
    bad = cnt = 0
    for o, hub, dst in itertools.product(lons, repeat=3):
        e = (o, hub, dst, rng.randint(0,23), rng.randint(0,60), rng.randint(0,60), rng.randint(0,60))
        cnt += 1
        t1, t2, h1, h2, n2, tr = run2(d2m, enc(*e))
        if block(t2) != expected(*e): bad += 1
        # Testa tambem na MT1 a cada 25 rodadas (625 total)
        if cnt % 25 == 0 and not chk(e)[0]: bad += 1
    print(f"15625 combinacoes de longitudes (MT2; 625 tambem MT1) -> Falhas: {bad}")

    # Teste 2: 1500 aleatorios
    bad = cnt = 0
    for _ in range(1500):
        D = lambda: rng.choice([0, rng.randint(0,5), rng.randint(0,60), rng.randint(0,150)])
        e = (rng.choice(lons), rng.choice(lons), rng.choice(lons), rng.randint(0,23), D(), D(), D())
        cnt += 1
        bad += not chk(e)[0]
    print(f"1500 aleatorios variados em MT1 e MT2 -> Falhas: {bad}")

    # Teste 3: Casos de borda
    edge = [(o,hu,ds,h0)+Dd for o in (-180,-15,0,15,180) for hu in (-180,0,180) 
            for ds in (-180,0,180) for h0 in (0,23) 
            for Dd in [(0,0,0),(1,0,0),(0,1,0),(0,0,1),(24,0,0),(23,1,0),(0,24,24),(48,48,48)]]
    bad = sum(not chk(e)[0] for e in edge)
    print(f"{len(edge)} casos de borda extremos -> Falhas: {bad}")

    print("\n[Estatísticas das Máquinas]")
    print('MT1: {} estados, {} transicoes'.format(len({k[0] for k in d1m}|{'halt'}), len(d1m)))
    print('MT2: {} estados, {} transicoes'.format(len({k[0] for k in d2m}|{'halt'}), len(d2m)))

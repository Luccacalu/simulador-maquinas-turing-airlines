import sys
from tm import *

def format_q(q):
    return f"{q[0]}{q[1]}" if isinstance(q, tuple) else str(q)

def print_trace1(tr):
    print(f"{'Passo':>5s} {'Est':>5s}   Fita")
    for step, q, t, h in tr:
        fita_str = ""
        max_idx = max(t.keys()) if t else 0
        for i in range(max_idx + 2):
            char = t.get(i, '_') if t.get(i, '_') != ' ' else '_'
            if i == h:
                fita_str += f"[{char}]"
            else:
                fita_str += char
        print(f"{step:5d} {format_q(q):5s}   {fita_str}")

def print_trace2(tr):
    print(f"{'Passo':>5s} {'Est':>5s}   Fita 1 (Entrada)                 Fita 2 (Saida)")
    for step, q, t1, h1, t2, h2 in tr:
        fita1_str = ""
        max1 = max(t1.keys()) if t1 else 0
        for i in range(max1 + 2):
            char = t1.get(i, '_') if t1.get(i, '_') != ' ' else '_'
            fita1_str += f"[{char}]" if i == h1 else char
            
        fita2_str = ""
        max2 = max(t2.keys()) if t2 else 0
        for i in range(max2 + 2):
            char = t2.get(i, '_') if t2.get(i, '_') != ' ' else '_'
            fita2_str += f"[{char}]" if i == h2 else char
            
        print(f"{step:5d} {format_q(q):5s}   {fita1_str:<30s} {fita2_str}")

if __name__ == "__main__":
    print("==========================================")
    print(" Simulador Turing Airlines")
    print("==========================================")
    
    if len(sys.argv) > 1:
        w = sys.argv[1]
    else:
        print("-> Nenhuma fita informada nos argumentos.")
        print("-> Rodando o exemplo minimo padrao (origem 15 L, d1=1).")
        w = "L####1|#"
        
    print(f"\nEntrada fornecida na fita: {w}\n")
    
    print("========== SIMULANDO MT1 (1 FITA) ==========")
    d1m = build_mt1()
    t, h, n, tr = run1(d1m, w, trace=True)
    print_trace1(tr)
    print(f"\n=> FINAL MT1: {block(t)} em {n} passos.\n")
    
    print("========== SIMULANDO MT2 (2 FITAS) =========")
    d2m = build_mt2()
    t1, t2, h1, h2, n, tr = run2(d2m, w, trace=True)
    print_trace2(tr)
    print(f"\n=> FINAL MT2: {block(t2)} em {n} passos.\n")
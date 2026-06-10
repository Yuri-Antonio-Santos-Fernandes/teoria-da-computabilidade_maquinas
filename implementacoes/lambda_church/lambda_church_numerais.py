# %% [cell 1]
"""
λ-Cálculo — Numerais de Church
Teoria da Computabilidade — CESUPA 2026

Ideia central:
  Um numeral de Church representa N como
  "aplique f exatamente N vezes sobre x":

  0 = λf.λx.x
  1 = λf.λx.f x
  2 = λf.λx.f(f x)
  3 = λf.λx.f(f(f x))

Operações:
  SUCC  — sucessor:      N → N+1
  ADD   — soma:          M + N
  MULT  — multiplicação: M * N
"""

# ─────────────────────────────────────────────
# 1. REPRESENTAÇÃO DOS TERMOS
# ─────────────────────────────────────────────

class Var:
    def __init__(self, name): self.name = name
    def __repr__(self): return self.name
    def clone(self): return Var(self.name)

class Abs:
    def __init__(self, param, body): self.param = param; self.body = body
    def __repr__(self): return f"(λ{self.param}.{self.body})"
    def clone(self): return Abs(self.param, self.body.clone())

class App:
    def __init__(self, func, arg): self.func = func; self.arg = arg
    def __repr__(self): return f"({self.func} {self.arg})"
    def clone(self): return App(self.func.clone(), self.arg.clone())


# ─────────────────────────────────────────────
# 2. VARIÁVEIS LIVRES
# ─────────────────────────────────────────────

def fv(t):
    if isinstance(t, Var): return {t.name}
    if isinstance(t, Abs): return fv(t.body) - {t.param}
    if isinstance(t, App): return fv(t.func) | fv(t.arg)


# ─────────────────────────────────────────────
# 3. SUBSTITUIÇÃO [var := val] captura-evitante
# ─────────────────────────────────────────────

_cnt = 0
def novo(base):
    global _cnt; _cnt += 1
    b = base.rstrip("0123456789_")
    return f"{b}_{_cnt}"

def subst(t, var, val):
    if isinstance(t, Var):
        return val.clone() if t.name == var else t.clone()
    if isinstance(t, App):
        return App(subst(t.func, var, val), subst(t.arg, var, val))
    if isinstance(t, Abs):
        if t.param == var:            # variável ligada: não penetra
            return t.clone()
        if t.param in fv(val):        # risco de captura: renomeia
            p2 = novo(t.param)
            b2 = subst(t.body, t.param, Var(p2))
            return Abs(p2, subst(b2, var, val))
        return Abs(t.param, subst(t.body, var, val))


# ─────────────────────────────────────────────
# 4. REDUÇÃO BETA — um passo de cada vez
# ─────────────────────────────────────────────

def passo(t):
    """Retorna (termo_reduzido, descrição) ou (None, '')."""
    if isinstance(t, Var): return None, ""
    if isinstance(t, Abs):
        r, d = passo(t.body)
        return (Abs(t.param, r), d) if r else (None, "")
    if isinstance(t, App):
        if isinstance(t.func, Abs):          # redex encontrado
            resultado = subst(t.func.body, t.func.param, t.arg)
            desc = f"substitui {t.func.param}"
            return resultado, desc
        r, d = passo(t.func)                 # reduz função primeiro
        if r: return App(r, t.arg), d
        r, d = passo(t.arg)                  # depois o argumento
        if r: return App(t.func, r), d
        return None, ""


# ─────────────────────────────────────────────
# 5. AVALIADOR COM RASTREAMENTO
# ─────────────────────────────────────────────

def reduzir(termo, label="", max_passos=40):
    print("=" * 55)
    print(f"  {label}")
    print("=" * 55)
    atual = termo.clone()
    print(f"  Passo 0 (inicial) : {atual}")
    for i in range(1, max_passos + 1):
        r, desc = passo(atual)
        if r is None: break
        print(f"  Passo {i} [{desc}]")
        print(f"           → {r}")
        atual = r
    n = decodificar(atual)
    print(f"\n  ✔ Forma normal : {atual}")
    print(f"  ✔ Valor decimal: {n}")
    print()
    return atual


# ─────────────────────────────────────────────
# 6. DECODIFICAÇÃO: Church → inteiro
# ─────────────────────────────────────────────

def decodificar(t):
    """
    Conta o número de aplicações de f em λf.λx.f^n(x).
    A forma normal de um numeral de Church sempre tem essa estrutura.
    """
    def contar(node):
        if isinstance(node, Abs):   # λf. ou λx. — desce no corpo
            return contar(node.body)
        if isinstance(node, App):   # (f algo) — conta +1 e desce no argumento
            return 1 + contar(node.arg)
        return 0                    # Var x — caso base
    return contar(t)


# ─────────────────────────────────────────────
# 7. NUMERAIS E OPERAÇÕES DE CHURCH
# ─────────────────────────────────────────────

def church(n):
    """Constrói λf.λx. f^n(x)."""
    corpo = Var("x")
    for _ in range(n):
        corpo = App(Var("f"), corpo)
    return Abs("f", Abs("x", corpo))

ZERO = church(0)   # λf.λx.x
UM   = church(1)   # λf.λx.f x
DOIS = church(2)   # λf.λx.f(f x)
TRES = church(3)   # λf.λx.f(f(f x))

# SUCC = λn.λf.λx. f (n f x)
SUCC = Abs("n", Abs("f", Abs("x",
    App(Var("f"), App(App(Var("n"), Var("f")), Var("x")))
)))

# ADD = λm.λn.λf.λx. m f (n f x)
ADD = Abs("m", Abs("n", Abs("f", Abs("x",
    App(App(Var("m"), Var("f")),
        App(App(Var("n"), Var("f")), Var("x")))
))))

# MULT = λm.λn.λf. m (n f)
MULT = Abs("m", Abs("n", Abs("f",
    App(Var("m"), App(Var("n"), Var("f")))
)))


# ─────────────────────────────────────────────
# 8. EXEMPLOS
# ─────────────────────────────────────────────

if __name__ == "__main__":

    print("\n" + "=" * 55)
    print("  NUMERAIS DE CHURCH — Definições formais")
    print("=" * 55)
    for nome, val in [("ZERO",ZERO),("UM",UM),("DOIS",DOIS),("TRES",TRES)]:
        print(f"  {nome:4s} = {val}")
    print(f"\n  SUCC = {SUCC}")
    print(f"  ADD  = {ADD}")
    print(f"  MULT = {MULT}")
    print()

    # Exemplo 1: SUCC ZERO → 1
    reduzir(App(SUCC.clone(), ZERO.clone()),
            "SUCC ZERO  →  esperado: 1")

    # Exemplo 2: SUCC UM → 2
    reduzir(App(SUCC.clone(), UM.clone()),
            "SUCC UM  →  esperado: 2")

    # Exemplo 3: ADD UM DOIS → 3
    reduzir(App(App(ADD.clone(), UM.clone()), DOIS.clone()),
            "ADD UM DOIS  →  esperado: 3")

    # Exemplo 4: ADD DOIS DOIS → 4
    reduzir(App(App(ADD.clone(), DOIS.clone()), DOIS.clone()),
            "ADD DOIS DOIS  →  esperado: 4")

    # Exemplo 5: MULT DOIS TRES → 6
    reduzir(App(App(MULT.clone(), DOIS.clone()), TRES.clone()),
            "MULT DOIS TRES  →  esperado: 6")

    # Exemplo 6: SUCC (ADD UM UM) → 3
    reduzir(App(SUCC.clone(), App(App(ADD.clone(), UM.clone()), UM.clone())),
            "SUCC (ADD UM UM)  →  esperado: 3")

    # Exemplo 7: ADD (SUCC DOIS) DOIS → 5
    reduzir(App(App(ADD.clone(), App(SUCC.clone(), DOIS.clone())), DOIS.clone()),
            "ADD (SUCC DOIS) DOIS  →  esperado: 5")

    # =========================================================================
    # CASOS DE FRONTEIRA E ENTRADAS DE VALIDAÇÃO (Exigência da Seção 5 da Lauda)
    # =========================================================================

    # Exemplo 8 (Caso de Fronteira): Multiplicação por ZERO (Elemento Nulo)
    reduzir(App(App(MULT.clone(), TRES.clone()), ZERO.clone()),
            "FRONTEIRA: MULT TRES ZERO  →  esperado: 0")

    # Exemplo 9 (Caso de Fronteira): Soma com ZERO (Elemento Neutro)
    reduzir(App(App(ADD.clone(), ZERO.clone()), DOIS.clone()),
            "FRONTEIRA: ADD ZERO DOIS  →  esperado: 2")

    # Exemplo 10 (Caso Inválido/Estrutural): Redução de variável livre isolada
    # Demonstra que o avaliador reconhece quando não há mais redexes possíveis.
    reduzir(Var("x"),
            "ESTRUTURAL/INVÁLIDO: Variável livre pura (Sem redex para reduzir)")

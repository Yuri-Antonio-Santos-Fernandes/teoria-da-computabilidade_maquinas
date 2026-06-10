# Rastreamento — λ-Cálculo com Numerais de Church

Modelo: λ-Cálculo não tipado com Numerais de Church.
Arquivos:

- `implementacoes/lambda_church/lambda_church_numerais.ipynb`
- `implementacoes/lambda_church/lambda_church_numerais.py`

## Estratégia de redução

O avaliador usa redução β em ordem normal: o redex mais à esquerda e mais externo é reduzido primeiro. A implementação representa termos por uma AST com `Var`, `Abs` e `App`, além de substituição com verificação de variáveis livres e conversão α quando necessário.

## Casos principais

| Expressão | Passos | Forma normal esperada | Resultado |
|---|---:|---|---:|
| `SUCC ZERO` | 3 | `λf.λx.f x` | 1 |
| `ADD UM DOIS` | 7 | `λf.λx.f(f(f x))` | 3 |
| `ADD DOIS DOIS` | 9 | `λf.λx.f(f(f(f x)))` | 4 |
| `MULT DOIS TRES` | 12 | `λf.λx.f(f(f(f(f(f x)))))` | 6 |
| `MULT TRES ZERO` | 7 | `λf.λx.x` | 0 |

## Caso de fronteira

`Var("x")` é um termo válido do λ-cálculo, mas não contém redex. Portanto, fica estável imediatamente e não deve ser tratado como numeral de Church válido para decodificação aritmética.

## Limitações

O crescimento dos termos intermediários pode tornar a execução pesada mesmo para números pequenos. Como se trata de λ-cálculo não tipado, também existem termos que não terminam, como `(λx.x x) (λx.x x)`.

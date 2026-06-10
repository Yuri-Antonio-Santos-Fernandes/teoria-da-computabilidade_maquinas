# Rastreamento — APD para expressões aritméticas

Modelo: Autômato com Pilha determinístico no JFLAP.
Arquivo: `implementacoes/apd_expressoes/pda_expressoes_aritmeticas_corrigido.jff`.

## Linguagem trabalhada

Expressões sintaticamente válidas sobre o alfabeto `{a,b,c,+,-,*,/,(,)}`, com parênteses balanceados e limite de aninhamento adotado pela implementação.

## Entrada aceita: `a+b`

| Passo | Estado | Entrada restante | Pilha | Ação |
|---:|---|---|---|---|
| 1 | q0 | `a+b` | `[Z]` | lê variável e vai para q1 |
| 2 | q1 | `+b` | `[Z]` | lê operador e vai para q2 |
| 3 | q2 | `b` | `[Z]` | lê variável e retorna para q1 |
| 4 | q1 | `ε` | `[Z]` | transição vazia para q9 |
| 5 | q9 | `ε` | `[Z]` | aceita por estado final |

## Entrada aceita: `(a+b)`

| Passo | Estado | Entrada restante | Pilha | Ação |
|---:|---|---|---|---|
| 1 | q0 | `(a+b)` | `[Z]` | lê `(` e empilha `P` |
| 2 | q3 | `a+b)` | `[P,Z]` | lê variável |
| 3 | q4 | `+b)` | `[P,Z]` | lê operador |
| 4 | q5 | `b)` | `[P,Z]` | lê variável |
| 5 | q4 | `)` | `[P,Z]` | lê `)` e desempilha `P` |
| 6 | q1 | `ε` | `[Z]` | transição vazia para q9 |
| 7 | q9 | `ε` | `[Z]` | aceita por estado final |

## Entrada rejeitada: `(b+)`

| Passo | Estado | Entrada restante | Pilha | Ação |
|---:|---|---|---|---|
| 1 | q0 | `(b+)` | `[Z]` | lê `(` e empilha `P` |
| 2 | q3 | `b+)` | `[P,Z]` | lê variável |
| 3 | q4 | `+)` | `[P,Z]` | lê operador |
| 4 | q5 | `)` | `[P,Z]` | não há transição válida para fechar após operador |
| 5 | — | — | — | rejeita |

## Observações

A máquina realiza validação sintática. Ela não calcula o valor da expressão e não aplica precedência entre operadores.

# Rastreamento — MT Não Determinística para Subset Sum em unário

Modelo: Máquina de Turing Não Determinística simulada por programa, com configurações e árvore de computação explícitas.
Arquivo: `implementacoes/mt_nao_deterministica_subset_sum/mtnd_subset_sum.py`.

## Problema reconhecido

Entrada no formato:

```text
aa#aaa#a=aaaa
```

Cada bloco de `a` representa um número em unário. A máquina aceita quando existe algum subconjunto dos números à esquerda cuja soma seja igual ao alvo à direita do símbolo `=`.

## Exemplo aceito

Entrada: `aa#aaa#a=aaaa`

Interpretação: números `[2, 3, 1]`, alvo `4`.

Ramo aceitante encontrado:

```text
-2 +3 +1
```

Esse ramo ignora o número 2, inclui o número 3 e inclui o número 1. A soma final é `4`, então a máquina aceita.

## Árvore resumida

```text
soma 0
├── inclui 2 → soma 2
│   ├── inclui 3 → soma 5
│   │   ├── inclui 1 → soma 6 → rejeita
│   │   └── ignora 1 → soma 5 → rejeita
│   └── ignora 3 → soma 2
│       ├── inclui 1 → soma 3 → rejeita
│       └── ignora 1 → soma 2 → rejeita
└── ignora 2 → soma 0
    ├── inclui 3 → soma 3
    │   ├── inclui 1 → soma 4 → aceita
    │   └── ignora 1 → soma 3 → rejeita
    └── ignora 3 → soma 0
        ├── inclui 1 → soma 1 → rejeita
        └── ignora 1 → soma 0 → rejeita
```

## Tabela de testes

| Entrada | Interpretação | Esperado |
|---|---|---|
| `aa#aaa#a=aaaa` | `{2,3,1}`, alvo 4 | aceita |
| `a#aa#aaa=aaaaaa` | `{1,2,3}`, alvo 6 | aceita |
| `aa#aaaa=aaa` | `{2,4}`, alvo 3 | rejeita |
| `aaa#aa=aaaa` | `{3,2}`, alvo 4 | rejeita |
| `a#aa#aaa=` | alvo vazio | rejeita |
| `aa##aaa=aaaa` | bloco vazio | rejeita |

## Comandos úteis

```bash
python implementacoes/mt_nao_deterministica_subset_sum/mtnd_subset_sum.py "aa#aaa#a=aaaa" --tree
python implementacoes/mt_nao_deterministica_subset_sum/mtnd_subset_sum.py --testes
python implementacoes/mt_nao_deterministica_subset_sum/mtnd_subset_sum.py --transicoes
```

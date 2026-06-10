# Trabalho AV2 — Teoria da Computabilidade

Projeto da disciplina Teoria da Computabilidade — CESUPA — Turma CC5MA.

## Modelos escolhidos

O projeto reúne três modelos computacionais distintos:

1. **Autômato com Pilha Determinístico (APD)**  
   Reconhecimento de expressões aritméticas sintaticamente válidas.

2. **λ-Cálculo com Numerais de Church**  
   Calculadora funcional baseada em redução β, com operações `SUCC`, `ADD` e `MULT`.

3. **Máquina de Turing Não Determinística**  
   Reconhecimento de instâncias de Subset Sum em unário por árvore de computação.

## Estrutura do repositório

```text
trabalho-av2-computabilidade/
│
├── README.md
├── uso_ia.md
├── referencias.md
│
├── slides/
│   └── .gitkeep
│
├── relatorio/
│   └── .gitkeep
│
├── implementacoes/
│   ├── apd_expressoes/
│   │   └── pda_expressoes_aritmeticas_corrigido.jff
│   │
│   ├── lambda_church/
│   │   ├── lambda_church_numerais.ipynb
│   │   └── lambda_church_numerais.py
│   │
│   └── mt_nao_deterministica_subset_sum/
│       └── mtnd_subset_sum.py
│
├── rastreamentos/
│   ├── rastreamento_apd.md
│   ├── rastreamento_lambda.md
│   ├── rastreamento_mtnd.md
│   └── rastreamento_mtnd_execucao_exemplo.txt
│
└── testes/
    ├── testes_apd_expressoes.csv
    ├── testes_lambda_church.csv
    └── testes_mtnd_subset_sum.csv
```

As pastas `slides/` e `relatorio/` foram mantidas apenas com `.gitkeep`, pois o relatório/documentação será consolidado em um único arquivo pela equipe.

## Como executar cada implementação

### 1. APD no JFLAP

Arquivo:

```text
implementacoes/apd_expressoes/pda_expressoes_aritmeticas_corrigido.jff
```

Passos:

1. Abrir o JFLAP.
2. Selecionar a opção de Autômato com Pilha.
3. Carregar o arquivo `.jff`.
4. Usar a simulação por entrada para testar cadeias como `a+b`, `(a+b)` e `((a-b)*c)`.

### 2. λ-Cálculo em Python/Jupyter

Arquivos:

```text
implementacoes/lambda_church/lambda_church_numerais.ipynb
implementacoes/lambda_church/lambda_church_numerais.py
```

Opções de execução:

```bash
python implementacoes/lambda_church/lambda_church_numerais.py
```

ou abrir o notebook no Jupyter/Google Colab.

### 3. MT Não Determinística para Subset Sum

Arquivo:

```text
implementacoes/mt_nao_deterministica_subset_sum/mtnd_subset_sum.py
```

Executar exemplo aceito:

```bash
python implementacoes/mt_nao_deterministica_subset_sum/mtnd_subset_sum.py "aa#aaa#a=aaaa" --tree
```

Executar testes internos:

```bash
python implementacoes/mt_nao_deterministica_subset_sum/mtnd_subset_sum.py --testes
```

Mostrar a relação de transição usada no simulador:

```bash
python implementacoes/mt_nao_deterministica_subset_sum/mtnd_subset_sum.py --transicoes
```

## Problemas resolvidos

### APD — expressões aritméticas

Reconhece expressões formadas por variáveis `a`, `b`, `c`, operadores `+`, `-`, `*`, `/` e parênteses. A máquina verifica a estrutura sintática, mas não calcula o valor da expressão.

### λ-Cálculo — Numerais de Church

Representa números naturais como funções de alta ordem e executa operações aritméticas por redução β. A implementação trabalha com sucessor, soma e multiplicação.

### MT Não Determinística — Subset Sum em unário

Recebe entradas no formato:

```text
bloco1#bloco2#...#blocok=alvo
```

Cada bloco é uma sequência de `a`. O tamanho do bloco representa um número. A máquina aceita se algum subconjunto dos números soma exatamente o alvo.

Exemplo:

```text
aa#aaa#a=aaaa
```

Interpretação: `{2, 3, 1}`, alvo `4`. A cadeia é aceita porque `3 + 1 = 4`.

## Testes e rastreamentos

Os testes ficam na pasta `testes/` e os rastreamentos ficam na pasta `rastreamentos/`.

Arquivos principais:

- `testes/testes_apd_expressoes.csv`
- `testes/testes_lambda_church.csv`
- `testes/testes_mtnd_subset_sum.csv`
- `rastreamentos/rastreamento_apd.md`
- `rastreamentos/rastreamento_lambda.md`
- `rastreamentos/rastreamento_mtnd.md`

## Integrantes

- João Pedro Almeida Follmann:
- Yuri Antonio Santos Fernandes:
- Samuel Paula Nunes Salheb:
- Arthur José Aviz Lima:
- Gabriel Cruz Filgueira:

# Declaração de uso de IA

## Ferramentas utilizadas

Foram utilizadas as ferramentas ChatGPT 5.5 e Claude, nas datas 03/06/2026 e 09/06/2026 respectivamente

## Finalidade

A ferramenta foi usada como apoio para:

- organizar ideias de implementação;
- revisar a estrutura do repositório;
- auxiliar na escrita inicial de comentários e arquivos auxiliares;
- sugerir testes e rastreamentos;
- apoiar a modelagem da Máquina de Turing Não Determinística para Subset Sum em unário.
- apoio na organização inicial do relatório e dos materiais auxiliares, como os slides.

## Resumo dos prompts

Foram solicitadas sugestões de máquinas/modelos adequados à proposta da atividade, revisão da documentação da APD, análise da máquina em λ-Cálculo, criação de uma estrutura de repositório e apoio na elaboração de uma Máquina de Turing Não Determinística com árvore de computação explícita. Também foi solicitado apoio para a criação e estruturação do relatório e dos slides utilizados na apresentação.

## Trechos aproveitados

Foram aproveitados rascunhos de estrutura, sugestões de teste, textos explicativos iniciais e uma versão base do simulador da MT Não Determinística.

## Revisão da equipe

Foi modificada a primeira versão feita da máquina APD que teve apoio da ferramenta Claude, com o intuito de melhorar a apresentação dela. As primeiras versões da documentação do GitHub também foram posteriormente revisadas e corrigidas pela equipe. Por fim, o slide teve novas adições para enriquecer a apresentação.

## Declaração

Declaramos que os materiais foram revisados pela equipe e que o uso de IA teve caráter de apoio, sem substituir o estudo, a validação técnica e a compreensão dos modelos computacionais utilizados.

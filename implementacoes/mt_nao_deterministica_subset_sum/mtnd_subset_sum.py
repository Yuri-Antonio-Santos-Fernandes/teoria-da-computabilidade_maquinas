#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Máquina de Turing Não Determinística — Subset Sum em unário
Teoria da Computabilidade — CESUPA

Problema reconhecido
--------------------
Entrada no formato:

    bloco1#bloco2#...#blocok=alvo

Cada bloco é uma sequência não vazia de 'a'. O tamanho do bloco representa
um número natural positivo em unário. A máquina aceita se existe algum
subconjunto dos blocos à esquerda cuja soma seja igual ao alvo.

Exemplo:
    aa#aaa#a=aaaa
    números = [2, 3, 1], alvo = 4
    aceita, pois 3 + 1 = 4.

O objetivo do código não é usar uma função pronta de subset sum, mas sim
representar explicitamente configurações, estados, transições e ramos de
computação de uma máquina não determinística.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable, List, Optional, Sequence, Tuple
import argparse
import csv
import sys


# Estados do modelo
Q0 = "q0_validar_entrada"
Q1 = "q1_escolher_numero"
Q2 = "q2_incluir_numero"
Q3 = "q3_ignorar_numero"
Q4 = "q4_comparar_soma"
QACC = "qacc_aceita"
QREJ = "qrej_rejeita"

ESTADOS = {Q0, Q1, Q2, Q3, Q4, QACC, QREJ}
ESTADO_INICIAL = Q0
ESTADOS_FINAIS = {QACC, QREJ}
ALFABETO_ENTRADA = {"a", "#", "="}


class ErroEntrada(ValueError):
    """Erro de sintaxe da entrada da máquina."""


@dataclass(frozen=True)
class Configuracao:
    """Configuração instantânea da máquina.

    A configuração representa o estado atual da computação, o índice do
    próximo número a ser decidido, a soma acumulada e o caminho de escolhas.
    O caminho usa +n para ramo que inclui n e -n para ramo que ignora n.
    """

    estado: str
    indice: int
    soma: int
    numeros: Tuple[int, ...]
    alvo: int
    caminho: Tuple[str, ...] = ()
    motivo: str = ""

    def eh_final(self) -> bool:
        return self.estado in ESTADOS_FINAIS

    def resumo(self) -> str:
        caminho = " ".join(self.caminho) if self.caminho else "∅"
        base = (
            f"{self.estado} | i={self.indice} | soma={self.soma} | "
            f"alvo={self.alvo} | caminho={caminho}"
        )
        return f"{base} | {self.motivo}" if self.motivo else base


@dataclass
class NoComputacao:
    """Nó da árvore de computação não determinística."""

    configuracao: Configuracao
    filhos: List["NoComputacao"] = field(default_factory=list)


@dataclass
class ResultadoExecucao:
    entrada: str
    numeros: Tuple[int, ...]
    alvo: int
    raiz: NoComputacao
    aceita: bool
    caminho_aceitante: Optional[Tuple[str, ...]]
    total_configuracoes: int
    ramos_finais: int


@dataclass(frozen=True)
class TransicaoFormal:
    origem: str
    condicao: str
    destino: str
    acao: str


TRANSICOES_FORMAIS = (
    TransicaoFormal(Q0, "entrada sintaticamente válida", Q1, "inicializar soma = 0 e índice = 0"),
    TransicaoFormal(Q0, "entrada inválida", QREJ, "parar rejeitando"),
    TransicaoFormal(Q1, "ainda existe número a decidir", Q2, "criar ramo que inclui o número atual"),
    TransicaoFormal(Q1, "ainda existe número a decidir", Q3, "criar ramo que ignora o número atual"),
    TransicaoFormal(Q1, "todos os números foram decididos", Q4, "comparar soma acumulada com alvo"),
    TransicaoFormal(Q2, "número atual = n", Q1, "somar n e avançar para o próximo índice"),
    TransicaoFormal(Q3, "número atual = n", Q1, "manter soma e avançar para o próximo índice"),
    TransicaoFormal(Q4, "soma == alvo", QACC, "aceitar por existência de ramo aceitante"),
    TransicaoFormal(Q4, "soma != alvo", QREJ, "rejeitar este ramo"),
)


def parse_entrada(entrada: str) -> Tuple[Tuple[int, ...], int]:
    """Converte uma entrada unária no formato blocos=alvo.

    Regras usadas no projeto:
    - Deve existir exatamente um '='.
    - A parte esquerda deve conter um ou mais blocos.
    - Cada bloco deve ser composto por uma ou mais letras 'a'.
    - O alvo deve ser uma sequência não vazia de 'a'.
    - Não são aceitos blocos vazios como em 'aa##a=aaa'.
    """

    entrada = entrada.strip()
    if not entrada:
        raise ErroEntrada("entrada vazia")

    simbolos_invalidos = set(entrada) - ALFABETO_ENTRADA
    if simbolos_invalidos:
        raise ErroEntrada(f"símbolos inválidos: {sorted(simbolos_invalidos)}")

    if entrada.count("=") != 1:
        raise ErroEntrada("a entrada deve conter exatamente um símbolo '='")

    esquerda, alvo_bruto = entrada.split("=", 1)
    if not esquerda:
        raise ErroEntrada("a lista de números à esquerda está vazia")
    if not alvo_bruto:
        raise ErroEntrada("o alvo está vazio")

    blocos = esquerda.split("#")
    if any(bloco == "" for bloco in blocos):
        raise ErroEntrada("existe bloco vazio entre separadores '#'")
    if any(set(bloco) != {"a"} for bloco in blocos):
        raise ErroEntrada("todos os blocos à esquerda devem conter apenas 'a'")
    if set(alvo_bruto) != {"a"}:
        raise ErroEntrada("o alvo deve conter apenas 'a'")

    numeros = tuple(len(bloco) for bloco in blocos)
    alvo = len(alvo_bruto)
    return numeros, alvo


def sucessores(config: Configuracao) -> List[Configuracao]:
    """Aplica a relação de transição não determinística δ."""

    if config.estado == Q0:
        return [
            Configuracao(
                estado=Q1,
                indice=0,
                soma=0,
                numeros=config.numeros,
                alvo=config.alvo,
                caminho=(),
                motivo="entrada validada; começa a árvore de escolhas",
            )
        ]

    if config.estado == Q1:
        if config.indice >= len(config.numeros):
            return [
                Configuracao(
                    estado=Q4,
                    indice=config.indice,
                    soma=config.soma,
                    numeros=config.numeros,
                    alvo=config.alvo,
                    caminho=config.caminho,
                    motivo="todos os números foram decididos",
                )
            ]

        atual = config.numeros[config.indice]
        return [
            Configuracao(
                estado=Q2,
                indice=config.indice,
                soma=config.soma,
                numeros=config.numeros,
                alvo=config.alvo,
                caminho=config.caminho,
                motivo=f"ramo não determinístico: incluir {atual}",
            ),
            Configuracao(
                estado=Q3,
                indice=config.indice,
                soma=config.soma,
                numeros=config.numeros,
                alvo=config.alvo,
                caminho=config.caminho,
                motivo=f"ramo não determinístico: ignorar {atual}",
            ),
        ]

    if config.estado == Q2:
        atual = config.numeros[config.indice]
        return [
            Configuracao(
                estado=Q1,
                indice=config.indice + 1,
                soma=config.soma + atual,
                numeros=config.numeros,
                alvo=config.alvo,
                caminho=config.caminho + (f"+{atual}",),
                motivo=f"incluiu {atual}",
            )
        ]

    if config.estado == Q3:
        atual = config.numeros[config.indice]
        return [
            Configuracao(
                estado=Q1,
                indice=config.indice + 1,
                soma=config.soma,
                numeros=config.numeros,
                alvo=config.alvo,
                caminho=config.caminho + (f"-{atual}",),
                motivo=f"ignorou {atual}",
            )
        ]

    if config.estado == Q4:
        if config.soma == config.alvo:
            return [
                Configuracao(
                    estado=QACC,
                    indice=config.indice,
                    soma=config.soma,
                    numeros=config.numeros,
                    alvo=config.alvo,
                    caminho=config.caminho,
                    motivo="soma igual ao alvo",
                )
            ]
        return [
            Configuracao(
                estado=QREJ,
                indice=config.indice,
                soma=config.soma,
                numeros=config.numeros,
                alvo=config.alvo,
                caminho=config.caminho,
                motivo="soma diferente do alvo",
            )
        ]

    return []


def construir_arvore(config: Configuracao, max_configuracoes: int, contador: List[int]) -> NoComputacao:
    """Constrói recursivamente a árvore de computação."""

    contador[0] += 1
    if contador[0] > max_configuracoes:
        raise RuntimeError(f"limite de {max_configuracoes} configurações excedido")

    no = NoComputacao(config)
    if config.eh_final():
        return no

    for proxima in sucessores(config):
        no.filhos.append(construir_arvore(proxima, max_configuracoes, contador))
    return no


def iterar_nos(raiz: NoComputacao) -> Iterable[NoComputacao]:
    yield raiz
    for filho in raiz.filhos:
        yield from iterar_nos(filho)


def primeiro_caminho_aceitante(raiz: NoComputacao) -> Optional[Tuple[str, ...]]:
    for no in iterar_nos(raiz):
        if no.configuracao.estado == QACC:
            return no.configuracao.caminho
    return None


def executar(entrada: str, max_configuracoes: int = 5000) -> ResultadoExecucao:
    """Executa a máquina sobre uma entrada."""

    try:
        numeros, alvo = parse_entrada(entrada)
        inicial = Configuracao(
            estado=Q0,
            indice=0,
            soma=0,
            numeros=numeros,
            alvo=alvo,
            caminho=(),
            motivo="configuração inicial",
        )
    except ErroEntrada as erro:
        inicial = Configuracao(
            estado=QREJ,
            indice=0,
            soma=0,
            numeros=(),
            alvo=0,
            caminho=(),
            motivo=f"entrada inválida: {erro}",
        )
        raiz = NoComputacao(inicial)
        return ResultadoExecucao(
            entrada=entrada,
            numeros=(),
            alvo=0,
            raiz=raiz,
            aceita=False,
            caminho_aceitante=None,
            total_configuracoes=1,
            ramos_finais=1,
        )

    contador = [0]
    raiz = construir_arvore(inicial, max_configuracoes=max_configuracoes, contador=contador)
    caminho = primeiro_caminho_aceitante(raiz)
    finais = sum(1 for no in iterar_nos(raiz) if no.configuracao.eh_final())
    return ResultadoExecucao(
        entrada=entrada,
        numeros=numeros,
        alvo=alvo,
        raiz=raiz,
        aceita=caminho is not None,
        caminho_aceitante=caminho,
        total_configuracoes=contador[0],
        ramos_finais=finais,
    )


def arvore_para_texto(no: NoComputacao, prefixo: str = "", ultimo: bool = True) -> str:
    """Gera uma representação textual da árvore de computação."""

    conector = "└── " if ultimo else "├── "
    linhas = [prefixo + conector + no.configuracao.resumo()]
    novo_prefixo = prefixo + ("    " if ultimo else "│   ")
    for i, filho in enumerate(no.filhos):
        linhas.append(arvore_para_texto(filho, novo_prefixo, i == len(no.filhos) - 1))
    return "\n".join(linhas)


def imprimir_transicoes() -> None:
    print("Relação de transição δ usada pelo simulador:\n")
    for t in TRANSICOES_FORMAIS:
        print(f"δ({t.origem}, {t.condicao}) -> {t.destino}; ação: {t.acao}")


def rodar_testes() -> int:
    casos = [
        ("aa#aaa#a=aaaa", True),
        ("a#aa#aaa=aaaaaa", True),
        ("aa#aaaa=aaa", False),
        ("aaa#aa=aaaa", False),
        ("a#aa#aaa=", False),
        ("aa##aaa=aaaa", False),
        ("aaaa=aaaa", True),
        ("aaaa=aa", False),
    ]

    falhas = 0
    print("Testes da MT Não Determinística para Subset Sum\n")
    for entrada, esperado in casos:
        resultado = executar(entrada)
        ok = resultado.aceita == esperado
        falhas += 0 if ok else 1
        status = "OK" if ok else "FALHOU"
        obtido = "aceita" if resultado.aceita else "rejeita"
        exp = "aceita" if esperado else "rejeita"
        print(f"[{status}] {entrada:<22} esperado={exp:<7} obtido={obtido}")

    return falhas


def salvar_csv_testes(caminho: str) -> None:
    casos = [
        ("aa#aaa#a=aaaa", "{2,3,1}, alvo 4", True),
        ("a#aa#aaa=aaaaaa", "{1,2,3}, alvo 6", True),
        ("aa#aaaa=aaa", "{2,4}, alvo 3", False),
        ("aaa#aa=aaaa", "{3,2}, alvo 4", False),
        ("a#aa#aaa=", "alvo vazio", False),
        ("aa##aaa=aaaa", "bloco vazio", False),
    ]
    with open(caminho, "w", newline="", encoding="utf-8") as arquivo:
        writer = csv.writer(arquivo)
        writer.writerow(["entrada", "interpretação", "esperado", "obtido", "caminho_aceitante"])
        for entrada, interpretacao, esperado in casos:
            resultado = executar(entrada)
            writer.writerow([
                entrada,
                interpretacao,
                "aceita" if esperado else "rejeita",
                "aceita" if resultado.aceita else "rejeita",
                " ".join(resultado.caminho_aceitante or ()),
            ])


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description="Simulador de MT Não Determinística para Subset Sum em unário."
    )
    parser.add_argument("entrada", nargs="?", help="Entrada no formato aa#aaa#a=aaaa")
    parser.add_argument("--tree", action="store_true", help="Mostra a árvore de computação")
    parser.add_argument("--transicoes", action="store_true", help="Mostra a relação formal de transição")
    parser.add_argument("--testes", action="store_true", help="Roda a suíte de testes interna")
    parser.add_argument("--max-configuracoes", type=int, default=5000, help="Limite de configurações")

    args = parser.parse_args(argv)

    if args.transicoes:
        imprimir_transicoes()
        print()

    if args.testes:
        return rodar_testes()

    if not args.entrada:
        parser.error("informe uma entrada ou use --testes")

    resultado = executar(args.entrada, max_configuracoes=args.max_configuracoes)
    print(f"Entrada: {resultado.entrada}")
    if resultado.numeros:
        print(f"Números: {list(resultado.numeros)}")
        print(f"Alvo: {resultado.alvo}")
    print(f"Resultado: {'ACEITA' if resultado.aceita else 'REJEITA'}")
    print(f"Configurações visitadas: {resultado.total_configuracoes}")
    print(f"Ramos finais: {resultado.ramos_finais}")
    if resultado.caminho_aceitante:
        print("Caminho aceitante:", " ".join(resultado.caminho_aceitante))

    if args.tree:
        print("\nÁrvore de computação:")
        print(arvore_para_texto(resultado.raiz))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

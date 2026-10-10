# ============================================================
# PRISMA — Algoritmos
#
# Arquivo: insertion_sort.py
#
# Responsabilidade:
#   - manter o estado do Insertion Sort;
#   - gerar o vetor inicial;
#   - executar um passo da ordenação;
#   - reiniciar a simulação.
# ============================================================

import random


class InsertionSort:
    """
    Representa uma simulação de Insertion Sort.

    Esta classe cuida somente da lógica e do estado
    do algoritmo. Ela não conhece a interface gráfica.
    """

    def __init__(self):
        """Cria uma nova simulação de Insertion Sort."""

        self.valores = []

        # Posição do elemento que estamos tentando inserir
        self.indice_atual = 1

        # Posição que estamos comparando
        self.indice_comparado = 0

        # Indica se o algoritmo terminou
        self.finalizado = False

        self.reiniciar()

    def reiniciar(self):
        """
        Gera um novo vetor e reinicia o estado
        do Insertion Sort.
        """

        self.valores = random.sample(
            range(1, 100),
            12
        )

        # A posição 0 já é considerada ordenada.
        self.indice_atual = 1

        # Começaremos comparando o segundo elemento
        # com o elemento anterior.
        self.indice_comparado = 0

        self.finalizado = False

    def proximo_passo(self):
        """
        Executa uma etapa do Insertion Sort.
        """

        # Se o algoritmo já terminou,
        # não fazemos mais nenhuma operação.
        if self.finalizado:
            return {
                "status": "finalizado"
            }

        # Se chegamos ao final do vetor,
        # todos os elementos estão ordenados.
        if self.indice_atual >= len(self.valores):

            self.finalizado = True

            return {
                "status": "finalizado"
            }

        # Valor que estamos tentando inserir
        valor_atual = self.valores[self.indice_atual]

        # ----------------------------------------------------
        # COMPARAÇÃO
        # ----------------------------------------------------

        if self.indice_comparado >= 0:

            valor_comparado = self.valores[
                self.indice_comparado
            ]

            # Se o elemento atual for menor que o anterior,
            # deslocamos o elemento anterior para a direita.
            if valor_atual < valor_comparado:

                # Nesta versão por etapas, a inserção usa trocas entre vizinhos.
                # O elemento menor caminha para a esquerda e o maior para a direita;
                # os índices guardados permitem continuar no próximo clique.
                self.valores[
                    self.indice_comparado
                ], self.valores[
                    self.indice_comparado + 1
                ] = (
                    self.valores[
                        self.indice_comparado + 1
                    ],
                    self.valores[
                        self.indice_comparado
                    ],
                )

                self.indice_comparado -= 1

                return {
                    "status": "troca",
                    "indice_atual": self.indice_atual,
                    "indice_comparado": self.indice_comparado + 1,
                    "valor_atual": valor_atual,
                    "valor_comparado": valor_comparado,
                }

            # O elemento já está na posição correta
            # dentro da parte ordenada.
            posicao_insercao = self.indice_comparado + 1

            self.indice_atual += 1
            self.indice_comparado = self.indice_atual - 1

            return {
                "status": "inserido",
                "indice_atual": self.indice_atual - 1,
                "posicao_insercao": posicao_insercao,
                "valor_atual": valor_atual,
            }

        # ----------------------------------------------------
        # ELEMENTO CHEGOU AO INÍCIO
        # ----------------------------------------------------

        self.indice_atual += 1
        self.indice_comparado = self.indice_atual - 1

        return {
            "status": "inserido",
            "indice_atual": self.indice_atual - 1,
            "posicao_insercao": 0,
            "valor_atual": valor_atual,
        }
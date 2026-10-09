# ============================================================
# PRISMA — Algoritmos
#
# Arquivo: selection_sort.py
#
# Responsabilidade:
#   - manter o estado do Selection Sort;
#   - gerar o vetor inicial;
#   - executar um passo da ordenação;
#   - reiniciar a simulação.
# ============================================================

import random


class SelectionSort:
    """
    Representa uma simulação de Selection Sort.

    Esta classe cuida somente da lógica e do estado
    do algoritmo. Ela não conhece a interface gráfica.
    """

    def __init__(self):
        """Cria uma nova simulação de Selection Sort."""

        self.valores = []

        # Posição que estamos tentando preencher
        self.indice_atual = 0

        # Índice do menor valor encontrado
        self.menor_indice = 0

        # Índice que está sendo comparado com o menor
        self.indice_comparado = 1

        self.finalizado = False

        self.reiniciar()

    def reiniciar(self):
        """
        Gera um novo vetor e reinicia o estado
        do Selection Sort.
        """

        self.valores = random.sample(
            range(1, 100),
            12
        )

        # Começamos procurando o menor valor
        # para ocupar a primeira posição.
        self.indice_atual = 0

        self.menor_indice = 0

        self.indice_comparado = 1

        self.finalizado = False

    def proximo_passo(self):
        """
        Executa uma etapa do Selection Sort.
        """

        # Se o algoritmo já terminou,
        # não fazemos mais nenhuma operação.
        if self.finalizado:
            return {
                "status": "finalizado"
            }

        # Se já percorremos todo o vetor,
        # a ordenação terminou.
        if self.indice_atual >= len(self.valores) - 1:

            self.finalizado = True

            return {
                "status": "finalizado"
            }

        # ----------------------------------------------------
        # FINAL DA BUSCA PELO MENOR
        # ----------------------------------------------------

        # Quando chegamos ao final da parte não ordenada,
        # temos o menor elemento encontrado.
        if self.indice_comparado >= len(self.valores):

            indice_menor = self.menor_indice

            valor_atual = self.valores[self.indice_atual]
            valor_menor = self.valores[indice_menor]

            # Realiza a troca.
            self.valores[self.indice_atual], self.valores[indice_menor] = (
                self.valores[indice_menor],
                self.valores[self.indice_atual],
            )

            # Guarda a posição que recebeu o menor valor.
            posicao_atual = self.indice_atual

            # Avança para a próxima posição do vetor.
            self.indice_atual += 1

            # O próximo menor começa na nova posição.
            self.menor_indice = self.indice_atual

            self.indice_comparado = self.indice_atual + 1

            return {
                "status": "troca",
                "indice_atual": posicao_atual,
                "menor_indice": indice_menor,
                "valor_atual": valor_atual,
                "valor_menor": valor_menor,
            }

        # ----------------------------------------------------
        # COMPARAÇÃO
        # ----------------------------------------------------

        indice_comparado = self.indice_comparado

        valor_menor = self.valores[self.menor_indice]
        valor_comparado = self.valores[indice_comparado]

        # Verifica se encontramos um novo menor valor.
        if valor_comparado < valor_menor:

            self.menor_indice = indice_comparado

            self.indice_comparado += 1

            return {
                "status": "novo_menor",
                "indice_atual": self.indice_atual,
                "menor_indice": self.menor_indice,
                "indice_comparado": indice_comparado,
                "valor_menor": valor_comparado,
                "valor_comparado": valor_comparado,
            }

        # Nenhum novo menor foi encontrado.
        self.indice_comparado += 1

        return {
            "status": "comparacao",
            "indice_atual": self.indice_atual,
            "menor_indice": self.menor_indice,
            "indice_comparado": indice_comparado,
            "valor_menor": valor_menor,
            "valor_comparado": valor_comparado,
        }
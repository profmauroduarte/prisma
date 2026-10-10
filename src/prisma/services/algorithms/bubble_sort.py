# ============================================================
# PRISMA — Algoritmos
#
# Arquivo: bubble_sort.py
#
# Responsabilidade:
#   - manter o estado do Bubble Sort;
#   - gerar o vetor inicial;
#   - executar um passo da ordenação;
#   - reiniciar a simulação.
# ============================================================

import random


class BubbleSort:
    """
    Representa uma simulação de Bubble Sort.

    Esta classe cuida somente da lógica e do estado
    do algoritmo. Ela não conhece a interface gráfica.
    """

    def __init__(self):
        """
        Cria uma nova simulação de Bubble Sort.
        """

        self.valores = []

        self.indice_atual = 0
        self.ultima_posicao = None

        self.finalizado = False
        self.trocou = False

        self.reiniciar()

    def reiniciar(self):
        """
        Cria um novo vetor e reinicia o estado
        da ordenação.
        """

        self.valores = random.sample(
            range(1, 100),
            12
        )

        self.indice_atual = 0
        self.ultima_posicao = len(self.valores) - 1

        self.finalizado = False
        self.trocou = False

    def proximo_passo(self):
        """
        Executa um passo do Bubble Sort.

        Compara dois elementos vizinhos e realiza
        uma troca quando necessário.
        """

        # Se a ordenação já terminou, não executamos novamente.
        if self.finalizado:
            return {
                "status": "finalizado",
                "indice": None,
                "proximo_indice": None,
                "troca": False,
            }

        # ----------------------------------------------------
        # FIM DA PASSADA ATUAL
        # ----------------------------------------------------

        if self.indice_atual >= self.ultima_posicao:

            # O maior elemento da parte analisada
            # já chegou ao final.
            self.ultima_posicao -= 1

            # Começamos uma nova passagem pelo vetor.
            self.indice_atual = 0
            self.trocou = False

            # Quando não há mais posições para comparar,
            # o vetor está ordenado.
            if self.ultima_posicao <= 0:
                self.finalizado = True

                return {
                    "status": "finalizado",
                    "indice": None,
                    "proximo_indice": None,
                    "troca": False,
                }

        # ----------------------------------------------------
        # COMPARAÇÃO
        # ----------------------------------------------------

        indice = self.indice_atual
        proximo_indice = indice + 1

        valor_atual = self.valores[indice]
        proximo_valor = self.valores[proximo_indice]

        # Avança para a próxima comparação.
        self.indice_atual += 1

        # ----------------------------------------------------
        # TROCA
        # ----------------------------------------------------

        if valor_atual > proximo_valor:

            # A atribuição simultânea troca os valores sem uma variável auxiliar:
            # o Python avalia o lado direito antes de alterar o lado esquerdo.
            self.valores[indice], self.valores[proximo_indice] = (
                self.valores[proximo_indice],
                self.valores[indice],
            )

            self.trocou = True

            return {
                "status": "troca",
                "indice": indice,
                "proximo_indice": proximo_indice,
                "valor_atual": valor_atual,
                "proximo_valor": proximo_valor,
                "troca": True,
            }

        # ----------------------------------------------------
        # SEM TROCA
        # ----------------------------------------------------

        return {
            "status": "comparacao",
            "indice": indice,
            "proximo_indice": proximo_indice,
            "valor_atual": valor_atual,
            "proximo_valor": proximo_valor,
            "troca": False,
        }
# ============================================================
# PRISMA — Algoritmos
#
# Arquivo: binary_search.py
#
# Responsabilidade:
#   - manter o estado da Busca Binária;
#   - gerar os dados ordenados da busca;
#   - executar um passo da busca;
#   - reiniciar a simulação.
# ============================================================

import random


class BuscaBinaria:
    """
    Representa uma simulação de Busca Binária.

    Esta classe cuida somente da lógica e do estado
    do algoritmo. Ela não conhece a interface gráfica.
    """

    def __init__(self):
        """
        Cria uma nova simulação de Busca Binária.
        """

        self.valores = []
        self.valor_procurado = None

        self.inicio = 0
        self.fim = 0
        self.meio = None

        self.posicao_analisada = None

        self.finalizado = False
        self.encontrado = False

        self.reiniciar()

    def reiniciar(self):
        """
        Cria um novo vetor ordenado e escolhe
        um novo valor procurado.

        Também reinicia os limites da busca.
        """

        self.valores = sorted(
            random.sample(
                range(1, 100),
                12
            )
        )

        self.valor_procurado = random.choice(
            self.valores
        )

        self.inicio = 0
        self.fim = len(self.valores) - 1
        self.meio = None

        self.posicao_analisada = None

        self.finalizado = False
        self.encontrado = False

    def proximo_passo(self):
        """
        Executa um passo da Busca Binária.

        A cada passo, calcula o meio do intervalo
        atualmente considerado e compara o valor
        encontrado com o valor procurado.

        Retorna informações sobre o passo realizado
        para que a interface possa apresentar o resultado.
        """

        # Se a busca já terminou, não executamos novamente.
        if self.finalizado:
            return {
                "status": "finalizado",
                "posicao": self.posicao_analisada,
                "valor": None,
                "inicio": self.inicio,
                "meio": self.meio,
                "fim": self.fim,
            }

        # ----------------------------------------------------
        # INTERVALO VÁLIDO
        # ----------------------------------------------------

        if self.inicio <= self.fim:

            # Calcula a posição central do intervalo.
            self.meio = (self.inicio + self.fim) // 2

            # Registra a posição analisada.
            self.posicao_analisada = self.meio

            # Obtém o valor da posição central.
            valor_atual = self.valores[self.meio]

            # ------------------------------------------------
            # VALOR ENCONTRADO
            # ------------------------------------------------

            if valor_atual == self.valor_procurado:

                self.finalizado = True
                self.encontrado = True

                return {
                    "status": "encontrado",
                    "posicao": self.meio,
                    "valor": valor_atual,
                    "inicio": self.inicio,
                    "meio": self.meio,
                    "fim": self.fim,
                }

            # ------------------------------------------------
            # VALOR PROCURADO É MAIOR
            # ------------------------------------------------

            if self.valor_procurado > valor_atual:

                self.inicio = self.meio + 1

                return {
                    "status": "maior",
                    "posicao": self.meio,
                    "valor": valor_atual,
                    "inicio": self.inicio,
                    "meio": self.meio,
                    "fim": self.fim,
                }

            # ------------------------------------------------
            # VALOR PROCURADO É MENOR
            # ------------------------------------------------

            self.fim = self.meio - 1

            return {
                "status": "menor",
                "posicao": self.meio,
                "valor": valor_atual,
                "inicio": self.inicio,
                "meio": self.meio,
                "fim": self.fim,
            }

        # ----------------------------------------------------
        # INTERVALO ESGOTADO
        # ----------------------------------------------------

        self.finalizado = True
        self.encontrado = False

        return {
            "status": "nao_encontrado",
            "posicao": self.posicao_analisada,
            "valor": None,
            "inicio": self.inicio,
            "meio": self.meio,
            "fim": self.fim,
        }
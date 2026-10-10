# ============================================================
# PRISMA — Algoritmos
#
# Arquivo: linear_search.py
#
# Responsabilidade:
#   - manter o estado da Busca Linear;
#   - gerar os dados da busca;
#   - executar um passo da busca;
#   - reiniciar a simulação.
# ============================================================

import random


class BuscaLinear:
    """
    Representa uma simulação de Busca Linear.

    Esta classe cuida somente da lógica e do estado
    do algoritmo. Ela não conhece a interface gráfica.
    """

    def __init__(self):
        """
        Cria uma nova simulação de Busca Linear.
        """

        self.valores = []
        self.valor_procurado = None
        self.indice_atual = 0
        self.posicao_analisada = None
        self.finalizado = False
        self.encontrado = False

        self.reiniciar()

    def reiniciar(self):
        """
        Cria um novo vetor e escolhe um novo valor procurado.

        Também retorna o estado da busca para o início.
        """

        # sample() gera valores sem repetição. A busca linear não exige
        # ordenação: ela examina cada posição em sequência.
        self.valores = random.sample(
            range(1, 100),
            12
        )

        # Escolher um valor do próprio vetor garante um alvo presente
        # na demonstração inicial.
        self.valor_procurado = random.choice(
            self.valores
        )

        self.indice_atual = 0
        self.posicao_analisada = None
        self.finalizado = False
        self.encontrado = False

    def proximo_passo(self):
        """
        Executa um passo da Busca Linear.

        Retorna informações sobre o passo realizado
        para que a interface possa apresentar o resultado.

        A classe não cria textos para a interface.
        Ela apenas informa o que aconteceu.
        """

        # Se a busca já terminou, não executamos novamente.
        if self.finalizado:
            return {
                "status": "finalizado",
                "posicao": self.posicao_analisada,
                "valor": None,
            }

        # Guarda a posição que será analisada.
        posicao = self.indice_atual

        # Obtém o valor daquela posição.
        valor_atual = self.valores[posicao]

        # Registra a posição analisada.
        self.posicao_analisada = posicao

        # ----------------------------------------------------
        # VALOR ENCONTRADO
        # ----------------------------------------------------

        if valor_atual == self.valor_procurado:

            self.finalizado = True
            self.encontrado = True

            return {
                "status": "encontrado",
                "posicao": posicao,
                "valor": valor_atual,
            }

        # ----------------------------------------------------
        # VALOR NÃO ENCONTRADO
        # ----------------------------------------------------

        if posicao < len(self.valores) - 1:

            # A próxima posição será analisada
            # no próximo clique.
            self.indice_atual += 1

            return {
                "status": "nao_encontrado",
                "posicao": posicao,
                "valor": valor_atual,
            }

        # ----------------------------------------------------
        # CHEGOU À ÚLTIMA POSIÇÃO
        # ----------------------------------------------------

        self.finalizado = True
        self.encontrado = False

        return {
            "status": "nao_encontrado",
            "posicao": posicao,
            "valor": valor_atual,
        }
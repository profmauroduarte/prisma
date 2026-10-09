# ============================================================
# PRISMA — Estruturas de Dados
#
# Arquivo: queue_structure.py
#
# Responsabilidade:
#   - manter o estado da fila;
#   - simular a entrada e a saída dos elementos;
#   - reiniciar a simulação.
# ============================================================

class Fila:
    """
    Representa uma simulação de fila.

    Mantém os dados e informa o resultado de cada passo
    para que a interface possa atualizar a visualização.
    """

    def __init__(self):
        """Cria uma nova simulação de fila."""

        self.reiniciar()

    def reiniciar(self):
        """Esvazia a fila e reinicia a etapa de inserção."""

        self.valores = []

        self.proximo_valor = 10
        self.capacidade = 5

        self.operacao = "enqueue"

    def proximo_passo(self):
        """
        Insere um elemento por passo até atingir a capacidade.

        Depois, remove um elemento por passo até esvaziar a fila.
        O primeiro elemento inserido é o primeiro a sair (FIFO).
        """


        # ====================================================
        # ENQUEUE — adicionando elementos
        # ====================================================

        if self.operacao == "enqueue":

            if len(self.valores) < self.capacidade:

                valor = self.proximo_valor

                self.valores.append(valor)

                self.proximo_valor += 10

                return {
                    "status": "enqueue",
                    "valor": valor,
                }

            # Ao atingir a capacidade, começa a etapa de remoção.
            self.operacao = "dequeue"

        # ====================================================
        # DEQUEUE — removendo elementos
        # ====================================================

        if self.operacao == "dequeue":

            if self.valores:

                # Remove o primeiro elemento inserido que ainda está na fila.
                valor = self.valores.pop(0)

                return {
                    "status": "dequeue",
                    "valor": valor,
                }

            return {
                "status": "finalizado"
            }
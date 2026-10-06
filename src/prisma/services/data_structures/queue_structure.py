class Fila:

    def __init__(self):
        self.reiniciar()

    def reiniciar(self):
        self.valores = []

        self.proximo_valor = 10
        self.capacidade = 5

        self.operacao = "enqueue"

    def proximo_passo(self):

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

            self.operacao = "dequeue"

        # ====================================================
        # DEQUEUE — removendo elementos
        # ====================================================

        if self.operacao == "dequeue":

            if self.valores:

                valor = self.valores.pop(0)

                return {
                    "status": "dequeue",
                    "valor": valor,
                }

            return {
                "status": "finalizado"
            }
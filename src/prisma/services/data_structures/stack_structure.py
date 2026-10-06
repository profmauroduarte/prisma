class Pilha:

    def __init__(self):
        self.reiniciar()

    def reiniciar(self):
        self.valores = []

        self.proximo_valor = 10
        self.capacidade = 5

        self.operacao = "push"

    def proximo_passo(self):

        # ====================================================
        # PUSH — adicionando elementos
        # ====================================================

        if self.operacao == "push":

            if len(self.valores) < self.capacidade:

                valor = self.proximo_valor

                self.valores.append(valor)

                self.proximo_valor += 10

                return {
                    "status": "push",
                    "valor": valor,
                }

            self.operacao = "pop"

        # ====================================================
        # POP — removendo elementos
        # ====================================================

        if self.operacao == "pop":

            if self.valores:

                valor = self.valores.pop()

                return {
                    "status": "pop",
                    "valor": valor,
                }

            return {
                "status": "finalizado"
            }
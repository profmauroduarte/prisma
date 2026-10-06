class Lista:

    def __init__(self):
        self.reiniciar()

    def reiniciar(self):
        """
        Cria uma nova lista e reinicia o estado
        da visualização.
        """

        self.valores = [
            10,
            20,
            30,
            40,
            50,
        ]

        self.indice_atual = 0

    def proximo_passo(self):
        """
        Avança um elemento por vez pela lista.
        """

        if self.indice_atual >= len(self.valores):

            return {
                "status": "finalizado"
            }

        indice = self.indice_atual
        valor = self.valores[indice]

        self.indice_atual += 1

        return {
            "status": "visitando",
            "indice": indice,
            "valor": valor,
        }
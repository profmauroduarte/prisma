# ============================================================
# PRISMA — Estruturas de Dados
#
# Arquivo: list_structure.py
#
# Responsabilidade:
#   - manter os valores da lista;
#   - percorrer um elemento por vez;
#   - reiniciar a simulação.
# ============================================================

class Lista:
    """
    Representa uma simulação de lista.

    Mantém os dados e informa o resultado de cada passo
    para que a interface possa atualizar a visualização.
    """

    def __init__(self):
        """Cria uma nova simulação de lista."""

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

        # O índice é o estado do percurso: cada chamada visita uma posição.
        # Reiniciar coloca o percurso no primeiro elemento, de índice zero.
        self.indice_atual = 0

    def proximo_passo(self):
        """
        Avança um elemento por vez pela lista.
        """

        # Quando todos os elementos foram visitados, encerra o percurso.
        if self.indice_atual >= len(self.valores):

            return {
                "status": "finalizado"
            }

        indice = self.indice_atual
        valor = self.valores[indice]

        # Guarda a próxima posição para o próximo passo.
        self.indice_atual += 1

        return {
            "status": "visitando",
            "indice": indice,
            "valor": valor,
        }
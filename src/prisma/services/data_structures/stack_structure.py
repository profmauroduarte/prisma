# ============================================================
# PRISMA — Estruturas de Dados
#
# Arquivo: stack_structure.py
#
# Responsabilidade:
#   - manter o estado da pilha;
#   - simular a entrada e a saída dos elementos;
#   - reiniciar a simulação.
# ============================================================

class Pilha:
    """
    Representa uma simulação de pilha.

    Mantém os dados e informa o resultado de cada passo
    para que a interface possa atualizar a visualização.
    """

    def __init__(self):
        """Cria uma nova simulação de pilha."""

        self.reiniciar()

    def reiniciar(self):
        """Esvazia a pilha e reinicia a etapa de inserção."""

        self.valores = []

        self.proximo_valor = 10
        # A capacidade limita esta demonstração, não a lista Python em si.
        self.capacidade = 5

        self.operacao = "push"

    def proximo_passo(self):
        """
        Insere um elemento por passo até atingir a capacidade.

        Depois, remove um elemento por passo até esvaziar a pilha.
        O último elemento inserido é o primeiro a sair (LIFO).
        """


        # ====================================================
        # PUSH — adicionando elementos
        # ====================================================

        if self.operacao == "push":

            if len(self.valores) < self.capacidade:

                valor = self.proximo_valor

                # O final da lista representa o topo. append() insere nesse topo
                # e pop() remove dele: último a entrar, primeiro a sair (LIFO).
                self.valores.append(valor)

                self.proximo_valor += 10

                return {
                    "status": "push",
                    "valor": valor,
                }

            # Ao atingir a capacidade, começa a etapa de remoção.
            self.operacao = "pop"

        # ====================================================
        # POP — removendo elementos
        # ====================================================

        if self.operacao == "pop":

            if self.valores:

                # Remove o último elemento inserido que ainda está na pilha.
                valor = self.valores.pop()

                return {
                    "status": "pop",
                    "valor": valor,
                }

            return {
                "status": "finalizado"
            }
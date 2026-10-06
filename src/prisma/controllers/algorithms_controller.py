from PySide6.QtWidgets import QLabel

from prisma.services.algorithms.linear_search import BuscaLinear
from prisma.services.algorithms.binary_search import BuscaBinaria
from prisma.services.algorithms.bubble_sort import BubbleSort
from prisma.services.algorithms.selection_sort import SelectionSort
from prisma.services.algorithms.insertion_sort import InsertionSort


class AlgorithmsController:
    """
    Controla a página de algoritmos do PRISMA.

    Responsabilidades:
    - criar e manter as instâncias dos algoritmos;
    - configurar a lista de algoritmos da interface;
    - conectar os sinais da página;
    - executar os algoritmos passo a passo;
    - atualizar as mensagens e visualizações.
    """

    def __init__(self, window):
        self.window = window

        # --------------------------------------------------------
        # Algoritmos
        # --------------------------------------------------------

        self.busca_linear = BuscaLinear()
        self.busca_binaria = BuscaBinaria()
        self.bubble_sort = BubbleSort()
        self.selection_sort = SelectionSort()
        self.insertion_sort = InsertionSort()

        # --------------------------------------------------------
        # Descrições
        # --------------------------------------------------------

        self.descricoes = {
            "Busca Linear":
                "Percorre o vetor elemento por elemento até "
                "encontrar o valor procurado.",

            "Busca Binária":
                "Divide o intervalo de busca ao meio a cada passo "
                "para localizar o valor procurado.",

            "Bubble Sort":
                "Compara elementos vizinhos e troca suas posições "
                "quando estão fora de ordem.",

            "Selection Sort":
                "Procura o menor elemento da parte não ordenada "
                "e o coloca na posição correta.",

            "Insertion Sort":
                "Insere cada elemento na posição correta dentro "
                "da parte já ordenada.",
        }

        self._configurar_ui()
        self._conectar_sinais()

        # Seleção inicial
        self.window.algorithmList.setCurrentRow(0)

    # ============================================================
    # CONFIGURAÇÃO
    # ============================================================

    def _configurar_ui(self):
        """Configura os elementos iniciais da página."""

        self.window.algorithmList.addItems([
            "Busca Linear",
            "Busca Binária",
            "Bubble Sort",
            "Selection Sort",
            "Insertion Sort",
        ])

    def _conectar_sinais(self):
        """Conecta os componentes da interface ao controller."""

        self.window.algorithmList.currentRowChanged.connect(
            self.selecionar_algoritmo
        )

        self.window.nextStepButton.clicked.connect(
            self.proximo_passo
        )

        self.window.resetAlgorithmButton.clicked.connect(
            self.reiniciar_algoritmo
        )

    # ============================================================
    # VISUALIZAÇÃO
    # ============================================================

    def atualizar_visualizacao(self):
        """Atualiza visualmente o vetor apresentado na tela."""

        while self.window.valuesLayout.count():

            item = self.window.valuesLayout.takeAt(0)

            if item.widget():
                item.widget().deleteLater()

        item_atual = self.window.algorithmList.currentItem()

        if item_atual is None:
            return

        algoritmo = item_atual.text()

        # --------------------------------------------------------
        # Busca Linear
        # --------------------------------------------------------

        if algoritmo == "Busca Linear":

            valores = self.busca_linear.valores
            posicao_analisada = self.busca_linear.posicao_analisada

            for indice, valor in enumerate(valores):

                if indice == posicao_analisada:
                    label = QLabel(f"▶ {valor}")
                else:
                    label = QLabel(str(valor))

                self.window.valuesLayout.addWidget(label)

        # --------------------------------------------------------
        # Busca Binária
        # --------------------------------------------------------

        elif algoritmo == "Busca Binária":

            valores = self.busca_binaria.valores
            posicao_analisada = self.busca_binaria.posicao_analisada

            for indice, valor in enumerate(valores):

                if indice == posicao_analisada:
                    label = QLabel(f"▶ {valor}")
                else:
                    label = QLabel(str(valor))

                self.window.valuesLayout.addWidget(label)

        # --------------------------------------------------------
        # Bubble Sort
        # --------------------------------------------------------

        elif algoritmo == "Bubble Sort":

            valores = self.bubble_sort.valores
            indice = self.bubble_sort.indice_atual - 1

            for posicao, valor in enumerate(valores):

                if posicao == indice:
                    label = QLabel(f"▶ {valor}")

                elif posicao == indice + 1:
                    label = QLabel(f"▶ {valor}")

                else:
                    label = QLabel(str(valor))

                self.window.valuesLayout.addWidget(label)

        # --------------------------------------------------------
        # Selection Sort
        # --------------------------------------------------------

        elif algoritmo == "Selection Sort":

            valores = self.selection_sort.valores
            indice_atual = self.selection_sort.indice_atual
            menor_indice = self.selection_sort.menor_indice
            indice_comparado = self.selection_sort.indice_comparado

            for posicao, valor in enumerate(valores):

                if posicao == menor_indice:
                    label = QLabel(f"▼ {valor}")

                elif posicao == indice_comparado:
                    label = QLabel(f"▶ {valor}")

                elif posicao == indice_atual:
                    label = QLabel(f"● {valor}")

                else:
                    label = QLabel(str(valor))

                self.window.valuesLayout.addWidget(label)

        # --------------------------------------------------------
        # Insertion Sort
        # --------------------------------------------------------

        elif algoritmo == "Insertion Sort":

            valores = self.insertion_sort.valores
            indice_atual = self.insertion_sort.indice_atual
            indice_comparado = self.insertion_sort.indice_comparado

            for posicao, valor in enumerate(valores):

                if posicao == indice_atual:
                    label = QLabel(f"● {valor}")

                elif posicao == indice_comparado:
                    label = QLabel(f"▶ {valor}")

                else:
                    label = QLabel(str(valor))

                self.window.valuesLayout.addWidget(label)

    # ============================================================
    # SELEÇÃO
    # ============================================================

    def selecionar_algoritmo(self, row):
        """
        Atualiza a área de visualização quando o usuário
        seleciona um algoritmo.
        """

        if row < 0:
            return

        item = self.window.algorithmList.item(row)

        if item is None:
            return

        algoritmo = item.text()

        self.window.visualizationTitle.setText(
            f"Visualização: {algoritmo}"
        )

        self.window.visualizationInfo.setText(
            self.descricoes[algoritmo]
        )

        if algoritmo == "Busca Linear":

            self.window.visualizationInfo.setText(
                self.descricoes[algoritmo]
                + "\n\n"
                + "Procurando por: "
                + f"{self.busca_linear.valor_procurado}"
            )

        elif algoritmo == "Busca Binária":

            self.window.visualizationInfo.setText(
                self.descricoes[algoritmo]
                + "\n\n"
                + "Procurando por: "
                + f"{self.busca_binaria.valor_procurado}"
            )

        self.atualizar_visualizacao()

    # ============================================================
    # PRÓXIMO PASSO
    # ============================================================

    def proximo_passo(self):
        """Executa um passo do algoritmo selecionado."""

        item = self.window.algorithmList.currentItem()

        if item is None:
            return

        algoritmo = item.text()

        # --------------------------------------------------------
        # Busca Linear
        # --------------------------------------------------------

        if algoritmo == "Busca Linear":

            resultado = self.busca_linear.proximo_passo()

            if resultado["status"] == "finalizado":

                self.window.visualizationInfo.setText(
                    f"Procurando por: "
                    f"{self.busca_linear.valor_procurado}\n\n"
                    "Busca já finalizada."
                )

                self.atualizar_visualizacao()
                return

            posicao = resultado["posicao"]
            valor = resultado["valor"]

            if resultado["status"] == "encontrado":

                self.window.visualizationInfo.setText(
                    f"Procurando por: "
                    f"{self.busca_linear.valor_procurado}\n"
                    f"Posição analisada: {posicao}\n"
                    f"Valor analisado: {valor}\n\n"
                    "✓ Valor encontrado!"
                )

                self.atualizar_visualizacao()
                return

            self.window.visualizationInfo.setText(
                f"Procurando por: "
                f"{self.busca_linear.valor_procurado}\n"
                f"Posição analisada: {posicao}\n"
                f"Valor analisado: {valor}\n\n"
                "✗ Não encontrado."
            )

            self.atualizar_visualizacao()
            return

        # --------------------------------------------------------
        # Busca Binária
        # --------------------------------------------------------

        if algoritmo == "Busca Binária":

            resultado = self.busca_binaria.proximo_passo()

            if resultado["status"] == "finalizado":

                self.window.visualizationInfo.setText(
                    f"Procurando por: "
                    f"{self.busca_binaria.valor_procurado}\n\n"
                    "Busca já finalizada."
                )

                self.atualizar_visualizacao()
                return

            valor = resultado["valor"]

            if resultado["status"] == "encontrado":

                self.window.visualizationInfo.setText(
                    f"Procurando por: "
                    f"{self.busca_binaria.valor_procurado}\n"
                    f"Início: {resultado['inicio']}\n"
                    f"Meio: {resultado['meio']}\n"
                    f"Fim: {resultado['fim']}\n"
                    f"Valor analisado: {valor}\n\n"
                    "✓ Valor encontrado!"
                )

                self.atualizar_visualizacao()
                return

            if resultado["status"] == "maior":

                self.window.visualizationInfo.setText(
                    f"Procurando por: "
                    f"{self.busca_binaria.valor_procurado}\n"
                    f"Início: {resultado['inicio']}\n"
                    f"Meio: {resultado['meio']}\n"
                    f"Fim: {resultado['fim']}\n"
                    f"Valor analisado: {valor}\n\n"
                    "→ O valor procurado é maior.\n"
                    "A busca continua à direita."
                )

                self.atualizar_visualizacao()
                return

            if resultado["status"] == "menor":

                self.window.visualizationInfo.setText(
                    f"Procurando por: "
                    f"{self.busca_binaria.valor_procurado}\n"
                    f"Início: {resultado['inicio']}\n"
                    f"Meio: {resultado['meio']}\n"
                    f"Fim: {resultado['fim']}\n"
                    f"Valor analisado: {valor}\n\n"
                    "← O valor procurado é menor.\n"
                    "A busca continua à esquerda."
                )

                self.atualizar_visualizacao()
                return

            self.window.visualizationInfo.setText(
                f"Procurando por: "
                f"{self.busca_binaria.valor_procurado}\n\n"
                "✗ Valor não encontrado."
            )

            self.atualizar_visualizacao()
            return

        # --------------------------------------------------------
        # Bubble Sort
        # --------------------------------------------------------

        if algoritmo == "Bubble Sort":

            resultado = self.bubble_sort.proximo_passo()

            if resultado["status"] == "finalizado":

                self.window.visualizationInfo.setText(
                    "Ordenação concluída!\n\n"
                    "✓ O vetor está ordenado."
                )

                self.atualizar_visualizacao()
                return

            indice = resultado["indice"]
            proximo_indice = resultado["proximo_indice"]

            valor_atual = resultado["valor_atual"]
            proximo_valor = resultado["proximo_valor"]

            if resultado["status"] == "troca":

                self.window.visualizationInfo.setText(
                    f"Comparando posições "
                    f"{indice} e {proximo_indice}\n"
                    f"Valores: {valor_atual} e "
                    f"{proximo_valor}\n\n"
                    "↔ Os valores foram trocados."
                )

            else:

                self.window.visualizationInfo.setText(
                    f"Comparando posições "
                    f"{indice} e {proximo_indice}\n"
                    f"Valores: {valor_atual} e "
                    f"{proximo_valor}\n\n"
                    "✓ Nenhuma troca necessária."
                )

            self.atualizar_visualizacao()
            return

        # --------------------------------------------------------
        # Selection Sort
        # --------------------------------------------------------

        if algoritmo == "Selection Sort":

            resultado = self.selection_sort.proximo_passo()

            if resultado["status"] == "finalizado":

                self.window.visualizationInfo.setText(
                    "Ordenação concluída!\n\n"
                    "✓ O vetor está ordenado."
                )

                self.atualizar_visualizacao()
                return

            if resultado["status"] == "troca":

                self.window.visualizationInfo.setText(
                    f"Posição atual: "
                    f"{resultado['indice_atual']}\n"
                    f"Menor valor encontrado: "
                    f"{resultado['valor_menor']}\n\n"
                    "↔ O menor valor foi colocado "
                    "na posição atual."
                )

                self.atualizar_visualizacao()
                return

            if resultado["status"] == "novo_menor":

                self.window.visualizationInfo.setText(
                    f"Posição atual: "
                    f"{resultado['indice_atual']}\n"
                    f"Comparando posição: "
                    f"{resultado['indice_comparado']}\n"
                    f"Valor comparado: "
                    f"{resultado['valor_comparado']}\n\n"
                    "▼ Novo menor valor encontrado!"
                )

                self.atualizar_visualizacao()
                return

            self.window.visualizationInfo.setText(
                f"Posição atual: "
                f"{resultado['indice_atual']}\n"
                f"Comparando posição: "
                f"{resultado['indice_comparado']}\n"
                f"Valor comparado: "
                f"{resultado['valor_comparado']}\n"
                f"Menor valor atual: "
                f"{resultado['valor_menor']}\n\n"
                "✓ O menor valor continua sendo "
                f"{resultado['valor_menor']}."
            )

            self.atualizar_visualizacao()
            return

        # --------------------------------------------------------
        # Insertion Sort
        # --------------------------------------------------------

        if algoritmo == "Insertion Sort":

            resultado = self.insertion_sort.proximo_passo()

            if resultado["status"] == "finalizado":

                self.window.visualizationInfo.setText(
                    "Ordenação concluída!\n\n"
                    "✓ O vetor está ordenado."
                )

                self.atualizar_visualizacao()
                return

            if resultado["status"] == "troca":

                self.window.visualizationInfo.setText(
                    f"Elemento atual: "
                    f"{resultado['valor_atual']}\n"
                    f"Comparando com: "
                    f"{resultado['valor_comparado']}\n\n"
                    "← O elemento maior foi deslocado "
                    "para a direita."
                )

                self.atualizar_visualizacao()
                return

            if resultado["status"] == "inserido":

                self.window.visualizationInfo.setText(
                    f"Elemento: "
                    f"{resultado['valor_atual']}\n"
                    f"Posição de inserção: "
                    f"{resultado['posicao_insercao']}\n\n"
                    "✓ Elemento inserido na posição correta."
                )

                self.atualizar_visualizacao()
                return

        self.window.visualizationInfo.setText(
            f"O algoritmo {algoritmo} "
            "ainda não foi implementado."
        )

    # ============================================================
    # REINICIAR
    # ============================================================

    def reiniciar_algoritmo(self):
        """Reinicia o algoritmo atualmente selecionado."""

        item = self.window.algorithmList.currentItem()

        if item is None:
            return

        algoritmo = item.text()

        algoritmos = {
            "Busca Linear": self.busca_linear,
            "Busca Binária": self.busca_binaria,
            "Bubble Sort": self.bubble_sort,
            "Selection Sort": self.selection_sort,
            "Insertion Sort": self.insertion_sort,
        }

        instancia = algoritmos.get(algoritmo)

        if instancia is None:
            return

        instancia.reiniciar()

        self.selecionar_algoritmo(
            self.window.algorithmList.currentRow()
        )
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QHBoxLayout, QVBoxLayout, QWidget

from prisma.services.data_structures.list_structure import Lista
from prisma.services.data_structures.stack_structure import Pilha
from prisma.services.data_structures.queue_structure import Fila


class DataStructuresController:
    """
    Controla a página de Estruturas de Dados do PRISMA.

    Responsabilidades:
    - criar e manter as instâncias das estruturas;
    - configurar a lista de estruturas da interface;
    - conectar os sinais da página;
    - executar as simulações passo a passo;
    - atualizar as mensagens e visualizações.
    """

    def __init__(self, window):
        self.window = window

        # --------------------------------------------------------
        # Estruturas
        # --------------------------------------------------------

        self.lista = Lista()
        self.pilha = Pilha()
        self.fila = Fila()

        self._configurar_ui()
        self._conectar_sinais()

        # Seleção inicial
        self.window.dataStructureList.setCurrentRow(0)

    # ============================================================
    # CONFIGURAÇÃO
    # ============================================================

    def _configurar_ui(self):
        """Configura os elementos iniciais da página."""

        self.window.dataStructureList.addItems([
            "Lista",
            "Pilha",
            "Fila",
        ])

    def _conectar_sinais(self):
        """Conecta os componentes da interface ao controller."""

        self.window.dataStructureList.currentRowChanged.connect(
            self.selecionar_estrutura
        )

        self.window.nextStepButton_2.clicked.connect(
            self.proximo_passo
        )

        self.window.resetDataStructureButton.clicked.connect(
            self.reiniciar_estrutura
        )

    # ============================================================
    # VISUALIZAÇÃO
    # ============================================================

    def atualizar_visualizacao(self):
        """
        Atualiza visualmente a estrutura de dados
        apresentada na tela.
        """

        # Remove a apresentação anterior antes de desenhar o novo estado.
        # Remover do layout não destrói o widget: deleteLater() faz essa limpeza
        # quando o Qt puder processá-la com segurança.
        while self.window.dataStructureValuesLayout.count():

            item = self.window.dataStructureValuesLayout.takeAt(0)

            if item.widget():
                item.widget().deleteLater()

        item_atual = self.window.dataStructureList.currentItem()

        if item_atual is None:
            return

        estrutura = item_atual.text()

        # --------------------------------------------------------
        # Lista
        # --------------------------------------------------------

        if estrutura == "Lista":

            for indice, valor in enumerate(self.lista.valores):

                # O serviço já avançou o índice para o próximo passo; subtraímos 1
                # para destacar o elemento que acabou de ser visitado.
                if indice == self.lista.indice_atual - 1:
                    label = QLabel(f"▶ {valor}")
                else:
                    label = QLabel(str(valor))

                self.window.dataStructureValuesLayout.addWidget(
                    label
                )

        # --------------------------------------------------------
        # Pilha
        # --------------------------------------------------------

        elif estrutura == "Pilha":

            pilha_widget = QWidget()

            pilha_layout = QVBoxLayout(pilha_widget)
            pilha_layout.setAlignment(Qt.AlignCenter)

            if self.pilha.valores:

                topo = QLabel("TOPO")
                topo.setAlignment(Qt.AlignCenter)
                pilha_layout.addWidget(topo)

                # Na lista Python, o topo fica no final. reversed() permite desenhá-lo
                # primeiro, no alto da tela, sem alterar a ordem dos dados.
                for valor in reversed(self.pilha.valores):

                    label = QLabel(str(valor))
                    label.setAlignment(Qt.AlignCenter)

                    pilha_layout.addWidget(label)

                base = QLabel("BASE")
                base.setAlignment(Qt.AlignCenter)

                pilha_layout.addWidget(base)

            self.window.dataStructureValuesLayout.addWidget(
                pilha_widget
            )

        # --------------------------------------------------------
        # Fila
        # --------------------------------------------------------

        elif estrutura == "Fila":

            fila_widget = QWidget()

            fila_layout = QVBoxLayout(fila_widget)
            fila_layout.setAlignment(Qt.AlignCenter)

            if self.fila.valores:

                indicadores_layout = QHBoxLayout()

                frente = QLabel("FRENTE")
                fim = QLabel("FIM")

                indicadores_layout.addWidget(frente)
                indicadores_layout.addStretch()
                indicadores_layout.addWidget(fim)

                fila_layout.addLayout(
                    indicadores_layout
                )

            valores_layout = QHBoxLayout()
            valores_layout.setAlignment(Qt.AlignCenter)

            for valor in self.fila.valores:

                label = QLabel(str(valor))

                valores_layout.addWidget(label)

            fila_layout.addLayout(
                valores_layout
            )

            if self.fila.valores:

                info = QLabel(
                    "← sai primeiro"
                    "                         "
                    "entra por último →"
                )

                info.setAlignment(Qt.AlignCenter)

                fila_layout.addWidget(info)

            self.window.dataStructureValuesLayout.addWidget(
                fila_widget
            )

    # ============================================================
    # SELEÇÃO
    # ============================================================

    def selecionar_estrutura(self, row):
        """
        Atualiza a área de visualização quando o usuário
        seleciona uma estrutura de dados.
        """

        if row < 0:
            return

        item = self.window.dataStructureList.item(row)

        if item is None:
            return

        estrutura = item.text()

        self.window.dataStructureVisualizationTitle.setText(
            f"Visualização: {estrutura}"
        )

        if estrutura == "Lista":

            self.window.dataStructureVisualizationInfo.setText(
                "Uma lista armazena elementos "
                "em uma sequência ordenada."
            )

        elif estrutura == "Pilha":

            self.window.dataStructureVisualizationInfo.setText(
                "Uma pilha segue o princípio LIFO: "
                "o último elemento inserido é o primeiro a sair."
            )

        elif estrutura == "Fila":

            self.window.dataStructureVisualizationInfo.setText(
                "Uma fila segue o princípio FIFO: "
                "o primeiro elemento inserido é o primeiro a sair."
            )

        self.atualizar_visualizacao()

    # ============================================================
    # PRÓXIMO PASSO
    # ============================================================

    def proximo_passo(self):
        """
        Executa o próximo passo da estrutura de dados
        atualmente selecionada.
        """

        item = self.window.dataStructureList.currentItem()

        if item is None:
            return

        estrutura = item.text()

        # --------------------------------------------------------
        # Lista
        # --------------------------------------------------------

        if estrutura == "Lista":

            resultado = self.lista.proximo_passo()

            if resultado["status"] == "finalizado":

                self.window.dataStructureVisualizationInfo.setText(
                    "Percorrendo a lista...\n\n"
                    "✓ Todos os elementos foram visitados."
                )

                self.atualizar_visualizacao()
                return

            self.window.dataStructureVisualizationInfo.setText(
                "Percorrendo a lista...\n"
                f"Posição: {resultado['indice']}\n"
                f"Valor: {resultado['valor']}"
            )

            self.atualizar_visualizacao()
            return

        # --------------------------------------------------------
        # Pilha
        # --------------------------------------------------------

        if estrutura == "Pilha":

            resultado = self.pilha.proximo_passo()

            if resultado["status"] == "push":

                self.window.dataStructureVisualizationInfo.setText(
                    "Inserindo elemento na pilha...\n\n"
                    "Operação: PUSH\n"
                    f"Valor: {resultado['valor']}"
                )

                self.atualizar_visualizacao()
                return

            if resultado["status"] == "pop":

                self.window.dataStructureVisualizationInfo.setText(
                    "Removendo elemento da pilha...\n\n"
                    "Operação: POP\n"
                    f"Valor: {resultado['valor']}"
                )

                self.atualizar_visualizacao()
                return

            if resultado["status"] == "finalizado":

                self.window.dataStructureVisualizationInfo.setText(
                    "A pilha está vazia.\n\n"
                    "✓ Simulação finalizada."
                )

                self.atualizar_visualizacao()
                return

        # --------------------------------------------------------
        # Fila
        # --------------------------------------------------------

        if estrutura == "Fila":

            resultado = self.fila.proximo_passo()

            if resultado["status"] == "enqueue":

                self.window.dataStructureVisualizationInfo.setText(
                    "Inserindo elemento na fila...\n\n"
                    "Operação: ENQUEUE\n"
                    f"Valor: {resultado['valor']}"
                )

                self.atualizar_visualizacao()
                return

            if resultado["status"] == "dequeue":

                self.window.dataStructureVisualizationInfo.setText(
                    "Removendo elemento da fila...\n\n"
                    "Operação: DEQUEUE\n"
                    f"Valor: {resultado['valor']}"
                )

                self.atualizar_visualizacao()
                return

            if resultado["status"] == "finalizado":

                self.window.dataStructureVisualizationInfo.setText(
                    "A fila está vazia.\n\n"
                    "✓ Simulação finalizada."
                )

                self.atualizar_visualizacao()
                return

    # ============================================================
    # REINICIAR
    # ============================================================

    def reiniciar_estrutura(self):
        """Reinicia a estrutura de dados selecionada."""

        item = self.window.dataStructureList.currentItem()

        if item is None:
            return

        estrutura = item.text()

        estruturas = {
            "Lista": self.lista,
            "Pilha": self.pilha,
            "Fila": self.fila,
        }

        instancia = estruturas.get(estrutura)

        if instancia is None:
            return

        instancia.reiniciar()

        self.selecionar_estrutura(
            self.window.dataStructureList.currentRow()
        )
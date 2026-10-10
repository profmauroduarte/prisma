from prisma.services.activities.activities_service import ActivitiesService


class ActivitiesController:
    """Filtra o catálogo e apresenta os detalhes da atividade selecionada."""

    MODULOS = {
        "Todos os módulos": None,
        "Playground": "playground",
        "DB Lab": "database",
        "API Explorer": "api",
    }

    def __init__(self, window):
        self.window = window
        self.service = ActivitiesService()
        self.atividades = []
        self.atividades_visiveis = []

        self.window.activitiesModuleComboBox.currentTextChanged.connect(self.filtrar)
        self.window.activitiesList.currentRowChanged.connect(self.exibir_atividade)

        try:
            self.atividades = self.service.carregar()
        except (OSError, ValueError) as erro:
            self.window.activitiesStatusLabel.setText(f"Erro ao carregar atividades: {erro}")
            self.window.activitiesModuleComboBox.setEnabled(False)
            return

        self.filtrar()

    def filtrar(self, texto=None):
        """Recria a lista com numeração a partir de 1 para o filtro atual."""
        modulo = self.MODULOS[self.window.activitiesModuleComboBox.currentText()]
        self.atividades_visiveis = [
            atividade for atividade in self.atividades
            if modulo is None or atividade["modulo"] == modulo
        ]

        # clear() também muda a seleção. Bloqueamos os sinais durante a
        # reconstrução para não consultar índices da lista anterior.
        lista = self.window.activitiesList
        lista.blockSignals(True)
        lista.clear()
        for numero, atividade in enumerate(self.atividades_visiveis, start=1):
            lista.addItem(f"{numero}. {atividade['titulo']}")
        lista.blockSignals(False)

        self.window.activitiesStatusLabel.setText(
            f"{len(self.atividades_visiveis)} atividade(s) disponível(is)."
        )
        if self.atividades_visiveis:
            lista.setCurrentRow(0)
        else:
            self.window.activitiesDetailsBrowser.setPlainText(
                "Nenhuma atividade disponível para este módulo."
            )

    def exibir_atividade(self, indice):
        if not 0 <= indice < len(self.atividades_visiveis):
            return

        atividade = self.atividades_visiveis[indice]
        modulo = next(
            nome for nome, codigo in self.MODULOS.items()
            if codigo == atividade["modulo"]
        )
        # Texto simples mantém código, SQL e JSON como foram cadastrados,
        # sem interpretar o conteúdo das atividades como HTML.
        self.window.activitiesDetailsBrowser.setPlainText(
            f"{atividade['titulo']}\nMódulo: {modulo}\n\n"
            f"Objetivo\n{atividade['objetivo']}\n\n"
            f"Instruções\n{atividade['instrucoes']}\n\n"
            f"Resultado esperado\n{atividade['resultado_esperado']}"
        )

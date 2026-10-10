# ============================================================
# PRISMA — Navegação
#
# Arquivo: navigation_controller.py
#
# Responsabilidade:
#   - conectar os botões de navegação;
#   - alternar entre as páginas da janela principal.
# ============================================================

from PySide6.QtWidgets import QSizePolicy


class NavigationController:
    """
    Controla a navegação entre as páginas principais do PRISMA.

    A interface utiliza um QStackedWidget para manter as diferentes
    páginas da aplicação. Este controller conecta os botões de
    navegação às respectivas páginas.
    """

    def __init__(self, window):
        """Guarda a janela principal e configura a navegação."""

        self.window = window

        self._connect_navigation()

    def _connect_navigation(self):
        """Associa cada botão à página correspondente da interface."""

        pages = {
            self.window.dashboardButton: self.window.dashboardPage,
            self.window.playgroundButton: self.window.playgroundPage,
            self.window.algorithmsButton: self.window.algorithmsPage,
            self.window.dataStructuresButton: self.window.dataStructuresPage,
            self.window.apiButton: self.window.apiPage,
            self.window.databaseButton: self.window.dbPage,
            self.window.concurrencyButton: self.window.concurrencyPage,
            self.window.activitiesButton: self.window.activitiesPage,
            self.window.settingsButton: self.window.settingsPage,
        }

        cards = {
            self.window.playgroundCard: self.window.playgroundPage,
            self.window.algorithmsCard: self.window.algorithmsPage,
            self.window.dataStructuresCard: self.window.dataStructuresPage,
            self.window.apiCard: self.window.apiPage,
            self.window.databaseCard: self.window.dbPage,
            self.window.concurrencyCard: self.window.concurrencyPage,
            self.window.activitiesCard: self.window.activitiesPage,
        }
        # Um QPushButton já oferece clique, foco e ativação pelo teclado.
        # A propriedade permite dar aparência de card usando QSS.
        for card in cards:
            card.setProperty("dashboardCard", True)
            card.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        for button in pages:
            button.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)
        pages.update(cards)

        # O argumento padrão guarda a página de cada botão no momento
        # da conexão, evitando que todos apontem para a última página.
        for button, page in pages.items():
            button.clicked.connect(
                lambda checked=False, target_page=page:
                    self.window.stackedWidget.setCurrentWidget(target_page)
            )

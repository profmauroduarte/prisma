# ============================================================
# PRISMA — Inicialização
#
# Arquivo: app.py
#
# Responsabilidade:
#   - criar a aplicação Qt;
#   - carregar a interface e registrar o editor personalizado;
#   - inicializar os controllers e exibir a janela principal.
# ============================================================

# imports 
import sys
from pathlib import Path
# imports do PySide6
from PySide6.QtCore import QFile
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication

# imports do projeto
from prisma.views.code_editor import CodeEditor
from prisma.controllers.navigation_controller import NavigationController
from prisma.services.playground.code_runner import CodeRunner
from prisma.controllers.algorithms_controller import AlgorithmsController
from prisma.controllers.data_structures_controller import DataStructuresController
from prisma.controllers.api_controller import ApiController
from prisma.controllers.database_controller import DatabaseController

def main():
    """Carrega a janela principal e inicia o loop de eventos do Qt."""

    app = QApplication(sys.argv)

    app.setApplicationName("PRISMA")

    # Caminho do diretório onde está o pacote "prisma"
    package_dir = Path(__file__).resolve().parent

    # Interface criada no Qt Designer
    ui_path = package_dir / "ui" / "main_window.ui"

    ui_file = QFile(str(ui_path))

    if not ui_file.open(QFile.ReadOnly):
        raise RuntimeError(
            f"Não foi possível abrir a interface: {ui_path}"
        )

    loader = QUiLoader()

    # Registra o widget customizado usado no Qt Designer
    loader.registerCustomWidget(CodeEditor)

    window = loader.load(ui_file)
    ui_file.close()

    if window is None:
        raise RuntimeError(
            f"Não foi possível carregar a interface: {loader.errorString()}"
        )

    # Os controllers conectam os componentes da janela às funcionalidades.
    navigation_controller = NavigationController(window)
    code_runner = CodeRunner(window)
    algorithms_controller = AlgorithmsController(window)
    data_structures_controller = DataStructuresController(window)
    api_controller = ApiController(window)
    database_controller = DatabaseController(window)
    
    window.show()

    # Mantém a aplicação respondendo aos eventos até a janela ser fechada.
    sys.exit(app.exec())
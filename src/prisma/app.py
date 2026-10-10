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
from prisma.controllers.playground_controller import PlaygroundController
from prisma.controllers.algorithms_controller import AlgorithmsController
from prisma.controllers.data_structures_controller import DataStructuresController
from prisma.controllers.api_controller import ApiController
from prisma.controllers.database_controller import DatabaseController

def main():
    """Carrega a janela principal e inicia o loop de eventos do Qt."""

    app = QApplication(sys.argv)

    # O nome também é usado pelo Qt ao determinar o diretório de dados
    # da aplicação, onde o DB Lab cria o banco padrão.
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
    # O .ui contém widgets promovidos para CodeEditor. O registro ensina
    # o loader a criar essa classe Python ao encontrar seu nome no XML.
    loader.registerCustomWidget(CodeEditor)

    window = loader.load(ui_file)
    ui_file.close()

    if window is None:
        raise RuntimeError(
            f"Não foi possível carregar a interface: {loader.errorString()}"
        )

    # Os controllers conectam os componentes da janela às funcionalidades.
    navigation_controller = NavigationController(window)
    playground_controller = PlaygroundController(window)
    algorithms_controller = AlgorithmsController(window)
    data_structures_controller = DataStructuresController(window)
    api_controller = ApiController(window)
    database_controller = DatabaseController(window)
    
    window.show()

    # Mantém a aplicação respondendo aos eventos até a janela ser fechada.
    # exec() inicia o loop de eventos: cliques, sinais e atualizações
    # são processados até a aplicação encerrar. Seu retorno é o código de saída.
    sys.exit(app.exec())

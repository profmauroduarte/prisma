# ============================================================
# PRISMA — Playground de Lógica
#
# Responsabilidade:
#   - conectar as ações da página ao serviço de execução;
#   - apresentar os resultados e limpar os campos da interface.
# ============================================================

from prisma.services.playground.code_runner import CodeRunner


class PlaygroundController:
    """Controla a interação com a página do Playground."""

    def __init__(self, window):
        self.window = window
        # O serviço não recebe a janela: sua entrada e sua saída são textos.
        self.code_runner = CodeRunner()

        # Passamos o método sem parênteses para executá-lo apenas no clique.
        self.window.runButton.clicked.connect(self.run_code)
        self.window.clearButton.clicked.connect(self.clear_output)

    def run_code(self):
        """Obtém o código do editor e apresenta o resultado do serviço."""
        code = self.window.codeEditor.toPlainText()
        result = self.code_runner.run_code(code)
        self.window.outputConsole.setPlainText(result)

    def clear_output(self):
        """Limpa o console e o editor do Playground."""
        self.window.outputConsole.clear()
        self.window.codeEditor.clear()

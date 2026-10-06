# ============================================================
# PRISMA — Playground de Lógica
#
# Arquivo: services/logic_playground.py
# Responsabilidade:
#   - executar o código Python digitado pelo aluno;
#   - capturar a saída do print();
#   - tratar erros de execução;
#   - limpar o console de saída.
# ============================================================


# ------------------------------------------------------------
# 1. Importações
# ------------------------------------------------------------

# io permite criar um buffer de texto para capturar
# aquilo que normalmente seria enviado para o console.
import io

# contextlib permite redirecionar temporariamente o stdout.
import contextlib

# traceback fornece informações sobre onde ocorreu um erro.
import traceback

# Tabela com as mensagens amigáveis dos erros.
from prisma.services.playground.error_messages import ERROR_MESSAGES

# ------------------------------------------------------------
# 2. Classe responsável pelo Playground
# ------------------------------------------------------------

class CodeRunner:

    def __init__(self, window):
        # Recebemos a janela principal da aplicação.
        #
        # O Playground já existe dentro do main_window.ui.
        # Portanto, não carregamos outro arquivo .ui aqui.
        self.window = window

        # O botão Executar chama o método run_code().
        self.window.runButton.clicked.connect(
            self.run_code
        )

        # O botão Limpar chama o método clear_output().
        self.window.clearButton.clicked.connect(
            self.clear_output
        )

    # --------------------------------------------------------
    # EXECUTA O CÓDIGO DIGITADO PELO ALUNO
    # --------------------------------------------------------

    def run_code(self):

        # Obtém o código digitado no editor.
        code = self.window.codeEditor.toPlainText()

        # Cria um buffer de texto para capturar
        # tudo que for enviado para print().
        output = io.StringIO()

        try:

            # Redireciona temporariamente o stdout
            # para o nosso buffer.
            with contextlib.redirect_stdout(output):

                # Executa o código Python digitado pelo aluno.
                exec(code)

            # Mostra no console o resultado capturado.
            self.window.outputConsole.setPlainText(
                output.getvalue()
            )

        except Exception as error:

            # Descobre o nome do tipo do erro.
            error_type = type(error).__name__

            # Procura uma explicação amigável para o aluno.
            message = ERROR_MESSAGES.get(
                error_type,
                "Ocorreu um erro durante a execução"
            )

            # Obtém as informações do traceback.
            traceback_info = traceback.extract_tb(
                error.__traceback__
            )

            # Obtém o número da última linha
            # registrada no traceback.
            line_number = traceback_info[-1].lineno

            # Mostra no console:
            #   - mensagem amigável;
            #   - linha do erro;
            #   - mensagem original do Python.
            self.window.outputConsole.setPlainText(
                f"{message}\n\n"
                f"Linha: {line_number}\n\n"
                f"Detalhes: {error}"
            )

    # --------------------------------------------------------
    # LIMPA O CONSOLE
    # --------------------------------------------------------

    def clear_output(self):

        # Limpa todo o conteúdo do console.
        self.window.outputConsole.clear()
        self.window.codeEditor.clear()
        
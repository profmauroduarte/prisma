# ============================================================
# PRISMA — Playground de Lógica
#
# Arquivo: services/playground/code_runner.py
# Responsabilidade:
#   - executar o código Python digitado pelo aluno;
#   - capturar a saída do print();
#   - tratar erros de execução;
#   - retornar o texto que será apresentado ao aluno.
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

    # --------------------------------------------------------
    # EXECUTA O CÓDIGO DIGITADO PELO ALUNO
    # --------------------------------------------------------

    def run_code(self, code):
        """Executa o código recebido e retorna a saída ou a mensagem de erro."""

        # Cria um buffer de texto para capturar
        # tudo que for enviado para print().
        output = io.StringIO()

        try:

            # Redireciona temporariamente o stdout
            # para o nosso buffer.
            # O redirecionamento vale apenas dentro do bloco with e é desfeito
            # mesmo se ocorrer um erro. A execução acontece na thread que o chamou.
            with contextlib.redirect_stdout(output):

                # Executa o código Python digitado pelo aluno.
                # exec() executa Python no próprio processo da aplicação.
                # Este mecanismo não oferece isolamento para código não confiável.
                exec(code)

            return output.getvalue()

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

            # Retorna para o controller:
            #   - mensagem amigável;
            #   - linha do erro;
            #   - mensagem original do Python.
            return (
                f"{message}\n\n"
                f"Linha: {line_number}\n\n"
                f"Detalhes: {error}"
            )

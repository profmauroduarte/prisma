# ============================================================
# PRISMA — Integração com APIs
#
# Arquivo: api_controller.py
#
# Responsabilidade:
#   - validar a URL e o corpo JSON da requisição;
#   - conectar as ações da página ao serviço de APIs;
#   - exibir respostas e mensagens de erro.
# ============================================================

import json

from prisma.services.api.api_client import ApiClient
from PySide6.QtWidgets import QMessageBox

class ApiController:
    """
    Controla a página de integração com APIs do PRISMA.

    Responsabilidades:
    - receber as ações do usuário;
    - solicitar requisições ao ApiClient;
    - exibir respostas e mensagens de erro.
    """

    def __init__(self, window):
        """Guarda a janela, cria o serviço de APIs e configura a página."""

        self.window = window
        self.api_client = ApiClient(window)

        self.metodo_atual = None

        self._conectar_sinais()

        self._atualizar_metodo()

    def _atualizar_metodo(self, metodo=None):
        """
        Habilita o corpo JSON para POST e PUT.
        Limpa o conteúdo para os métodos que não utilizam corpo.
        """

        metodo = self.window.apiMethodComboBox.currentText()

        usa_corpo = metodo in ("POST", "PUT")

        self.window.apiBodyInput.setEnabled(usa_corpo)
        self.window.apiBodyLabel.setEnabled(usa_corpo)

        if not usa_corpo:
            self.window.apiBodyInput.clear()

    def _conectar_sinais(self):
        """Conecta as ações da interface e os resultados do serviço de APIs."""

        self.window.apiMethodComboBox.currentTextChanged.connect(
            self._atualizar_metodo
        )
        self.window.apiSendButton.clicked.connect(
            self.enviar_requisicao
        )

        self.api_client.resposta_recebida.connect(
            self.exibir_resposta
        )

        self.api_client.erro_ocorrido.connect(
            self.exibir_erro
        )

    def enviar_requisicao(self):
        """Valida os dados e envia a requisição pelo método selecionado."""

        url = self.window.apiUrlInput.text().strip()
        metodo = self.window.apiMethodComboBox.currentText()

        if not url:
            self.window.apiStatusLabel.setText(
                "Informe uma URL para realizar a requisição."
            )
            return

        if not url.startswith(("http://", "https://")):
            self.window.apiStatusLabel.setText(
                "A URL deve começar com http:// ou https://."
            )
            return

        # Valida o JSON antes de iniciar uma requisição que utiliza corpo.
        dados_json = None

        if metodo in ("POST", "PUT"):
            texto = self.window.apiBodyInput.toPlainText().strip()

            if not texto:
                self.window.apiStatusLabel.setText(
                    "Informe o JSON que será enviado."
                )
                return

            try:
                dados_json = json.loads(texto)
            except json.JSONDecodeError as erro:
                self.window.apiStatusLabel.setText(
                    f"JSON inválido: {erro.msg} "
                    f"(linha {erro.lineno}, coluna {erro.colno})."
                )
                return

        # Guarda o método para interpretar a resposta e bloqueia novos envios
        # enquanto a requisição está em andamento.
        self.metodo_atual = metodo
        self.window.apiSendButton.setEnabled(False)
        self.window.apiStatusLabel.setText(
            "Enviando requisição..."
        )
        self.window.apiResponseOutput.clear()

        if metodo == "GET":
            self.api_client.get(url)

        elif metodo == "POST":
            corpo = json.dumps(
                dados_json,
                ensure_ascii=False,
            )
            self.api_client.post(url, corpo)

        elif metodo == "PUT":
            corpo = json.dumps(
                dados_json,
                ensure_ascii=False,
            )
            self.api_client.put(url, corpo)

        # A exclusão só é enviada após a confirmação na interface.
        elif metodo == "DELETE":
            resposta = QMessageBox.question(
                self.window,
                "Confirmar exclusão",
                f"Deseja realmente excluir o recurso?\n\n{url}",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No,
            )

            if resposta == QMessageBox.Yes:
                self.api_client.delete(url)
            else:
                self.window.apiSendButton.setEnabled(True)
                self.window.apiStatusLabel.setText(
                    "Exclusão cancelada pelo usuário."
                )

        else:
            self.window.apiSendButton.setEnabled(True)
            self.window.apiStatusLabel.setText(
                f"Método HTTP não suportado: {metodo}"
            )

    def exibir_resposta(self, status, conteudo):
        """Exibe o status HTTP e formata a resposta quando ela contém JSON."""

        self.window.apiSendButton.setEnabled(True)

        self.window.apiStatusLabel.setText(
            f"Status HTTP: {status}"
        )

        if self.metodo_atual == "DELETE" and 200 <= status < 300:
            self.window.apiResponseOutput.setPlainText(
                "Recurso excluído com sucesso!\n\n"
                f"Status HTTP: {status}\n\n"
                "O servidor confirmou a exclusão do recurso.\n"
                "Você pode realizar um GET na mesma URL "
                "para verificar."
            )
            return

        try:
            dados = json.loads(conteudo)

            conteudo_formatado = json.dumps(
                dados,
                indent=4,
                ensure_ascii=False,
            )

        except json.JSONDecodeError:
            # Respostas sem JSON são exibidas com o texto recebido.
            conteudo_formatado = conteudo

        self.window.apiResponseOutput.setPlainText(
            conteudo_formatado
        )
    def exibir_erro(self, mensagem):
        """Exibe o erro de comunicação e libera o envio de outra requisição."""

        self.window.apiSendButton.setEnabled(True)

        self.window.apiStatusLabel.setText(
            "Erro ao realizar requisição."
        )

        self.window.apiResponseOutput.setPlainText(
            mensagem
        )
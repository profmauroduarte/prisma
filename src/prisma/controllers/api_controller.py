import json

from prisma.services.api.api_client import ApiClient


class ApiController:
    """
    Controla a página de integração com APIs do PRISMA.

    Responsabilidades:
    - receber as ações do usuário;
    - solicitar requisições ao ApiClient;
    - exibir respostas e mensagens de erro.
    """

    def __init__(self, window):
        self.window = window
        self.api_client = ApiClient(window)

        self._conectar_sinais()

    def _conectar_sinais(self):
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
        url = self.window.apiUrlInput.text().strip()

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

        self.window.apiSendButton.setEnabled(False)
        self.window.apiStatusLabel.setText(
            "Enviando requisição..."
        )
        self.window.apiResponseOutput.clear()

        self.api_client.get(url)

    def exibir_resposta(self, status, conteudo):
        self.window.apiSendButton.setEnabled(True)

        self.window.apiStatusLabel.setText(
            f"Status HTTP: {status}"
        )

        try:
            dados = json.loads(conteudo)

            conteudo_formatado = json.dumps(
                dados,
                indent=4,
                ensure_ascii=False,
            )

        except json.JSONDecodeError:
            conteudo_formatado = conteudo

        self.window.apiResponseOutput.setPlainText(
            conteudo_formatado
        )

    def exibir_erro(self, mensagem):
        self.window.apiSendButton.setEnabled(True)

        self.window.apiStatusLabel.setText(
            "Erro ao realizar requisição."
        )

        self.window.apiResponseOutput.setPlainText(
            mensagem
        )
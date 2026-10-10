# ============================================================
# PRISMA — Integração com APIs
#
# Arquivo: api_client.py
#
# Responsabilidade:
#   - enviar requisições HTTP sem bloquear a interface;
#   - processar respostas e erros de comunicação;
#   - informar os resultados por meio de sinais do Qt.
# ============================================================

from PySide6.QtCore import QObject, Signal, QUrl, QByteArray
from PySide6.QtNetwork import (
    QNetworkAccessManager,
    QNetworkRequest,
    QNetworkReply,
)


class ApiClient(QObject):
    """
    Serviço responsável pela comunicação com APIs HTTP.

    Utiliza a infraestrutura assíncrona do Qt para realizar
    requisições sem bloquear a interface gráfica.
    """

    # Sinais transportam resultados ao controller sem o serviço conhecer
    # os widgets: aqui enviamos o status HTTP e o corpo da resposta.
    resposta_recebida = Signal(int, str)
    erro_ocorrido = Signal(str)

    def __init__(self, parent=None):
        """Cria o gerenciador de rede vinculado ao objeto Qt."""

        super().__init__(parent)

        # O parent vincula o ciclo de vida do gerenciador a este objeto Qt.
        # A rede trabalha de forma assíncrona, mantendo a interface responsiva.
        self.manager = QNetworkAccessManager(self)

    def get(self, url):
        """
        Envia uma requisição GET para a URL informada.
        """

        request = QNetworkRequest(QUrl(url))

        reply = self.manager.get(request)

        # Processa a resposta quando o Qt sinaliza o fim da requisição.
        reply.finished.connect(
            lambda: self._processar_resposta(reply)
        )

    def post(self, url, dados):
        """
        Envia uma requisição POST com um corpo JSON.

        Parâmetros:
        - url: endereço da API.
        - dados: string contendo o JSON a ser enviado.
        """

        request = QNetworkRequest(QUrl(url))

        request.setHeader(
            QNetworkRequest.ContentTypeHeader,
            "application/json",
        )

        # HTTP envia bytes. encode() transforma o texto JSON em UTF-8
        # e QByteArray fornece o formato esperado pela API do Qt.
        corpo = QByteArray(dados.encode("utf-8"))

        reply = self.manager.post(request, corpo)

        reply.finished.connect(
            lambda: self._processar_resposta(reply)
        )

    def put(self, url, dados):
        """
        Envia uma requisição PUT com um corpo JSON.

        Utilizado para substituir a representação
        de um recurso existente.
        """

        request = QNetworkRequest(QUrl(url))

        request.setHeader(
            QNetworkRequest.ContentTypeHeader,
            "application/json",
        )

        corpo = QByteArray(dados.encode("utf-8"))

        reply = self.manager.put(request, corpo)

        reply.finished.connect(
            lambda: self._processar_resposta(reply)
        )
    def delete(self, url):
        """
        Envia uma requisição DELETE para remover um recurso.
        """
        request = QNetworkRequest(QUrl(url))

        reply = self.manager.deleteResource(request)

        reply.finished.connect(
            lambda: self._processar_resposta(reply)
        )

    def _processar_resposta(self, reply):
        """
        Processa a resposta após a conclusão da requisição.
        """

        # O código HTTP descreve a resposta do servidor, como 200 ou 404.
        # Uma falha antes de receber resposta pode não ter status HTTP.
        status = reply.attribute(
            QNetworkRequest.HttpStatusCodeAttribute
        )

        # readAll() lê os bytes disponíveis. errors="replace" permite
        # exibir o texto mesmo se houver bytes inválidos em UTF-8.
        conteudo = bytes(reply.readAll()).decode(
            "utf-8",
            errors="replace",
        )

        if reply.error() != QNetworkReply.NoError:
            # Respostas HTTP 4xx/5xx também podem trazer um
            # corpo útil, então as mantemos para visualização.
            if status is None:
                self.erro_ocorrido.emit(reply.errorString())
                # Agenda a liberação da resposta após comunicar a falha.
                # O Qt fará a destruição ao processar os próximos eventos.
                reply.deleteLater()
                return

        # Informa o status e o conteúdo ao controller da página.
        self.resposta_recebida.emit(
            int(status) if status is not None else 0,
            conteudo,
        )

        reply.deleteLater()

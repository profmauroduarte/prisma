from PySide6.QtCore import QObject, Signal, QUrl
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

    resposta_recebida = Signal(int, str)
    erro_ocorrido = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.manager = QNetworkAccessManager(self)

    def get(self, url):
        """
        Envia uma requisição GET para a URL informada.
        """

        request = QNetworkRequest(QUrl(url))

        reply = self.manager.get(request)

        reply.finished.connect(
            lambda: self._processar_resposta(reply)
        )

    def _processar_resposta(self, reply):
        """
        Processa a resposta após a conclusão da requisição.
        """

        status = reply.attribute(
            QNetworkRequest.HttpStatusCodeAttribute
        )

        conteudo = bytes(reply.readAll()).decode(
            "utf-8",
            errors="replace",
        )

        if reply.error() != QNetworkReply.NoError:
            # Respostas HTTP 4xx/5xx também podem trazer um
            # corpo útil, então as mantemos para visualização.
            if status is None:
                self.erro_ocorrido.emit(reply.errorString())
                reply.deleteLater()
                return

        self.resposta_recebida.emit(
            int(status) if status is not None else 0,
            conteudo,
        )

        reply.deleteLater()
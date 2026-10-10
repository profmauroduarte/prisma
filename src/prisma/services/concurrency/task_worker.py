# A tarefa não conhece os widgets. Ela informa o progresso por um sinal
# e o controller decide como apresentar esse valor na interface.
from PySide6.QtCore import QThread, Signal


class TaskWorker(QThread):
    """Simula uma tarefa com duração configurável e etapas de 100 ms."""

    progresso = Signal(int)

    def __init__(self, parent=None, duracao=20):
        super().__init__(parent)
        self.duracao = duracao

    def run(self):
        # start() chama run() em outra thread. Chamar run() diretamente
        # executaria este código na thread de quem fez a chamada.
        total_etapas = self.duracao * 10
        ultimo_percentual = 0
        for etapa in range(1, total_etapas + 1):
            if self.isInterruptionRequested():
                return

            # A espera representa uma etapa demorada e ocorre somente
            # nesta thread; o loop de eventos da interface continua livre.
            self.msleep(100)

            # Verifica novamente para não emitir progresso após um pedido
            # de encerramento recebido durante a espera.
            if self.isInterruptionRequested():
                return

            # Converte a fração concluída em percentual, qualquer que seja
            # a duração. Emite somente quando o percentual muda.
            percentual = etapa * 100 // total_etapas
            if percentual != ultimo_percentual:
                self.progresso.emit(percentual)
                ultimo_percentual = percentual

        # O Qt emite finished automaticamente quando run() termina.

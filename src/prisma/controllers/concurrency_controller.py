from PySide6.QtCore import QEvent, QObject, Slot

from prisma.services.concurrency.task_worker import TaskWorker


class ConcurrencyController(QObject):
    """Controla o progresso e o ciclo de vida da demonstração de concorrência."""

    def __init__(self, window, settings_service=None):
        super().__init__(window)
        self.window = window
        self.worker = None
        self.settings_service = settings_service
        self.cancelamento_solicitado = False

        self.window.concurrencyStageLabel.setText(
            "Durante a tarefa, navegue entre as páginas para observar "
            "que a interface continua respondendo."
        )
        self.window.concurrencyStartButton.clicked.connect(self.iniciar_tarefa)
        self.window.concurrencyCancelButton.clicked.connect(self.cancelar_tarefa)
        self.window.concurrencyCancelButton.setEnabled(False)

        # O filtro permite encerrar a thread antes de a janela ser fechada.
        self.window.installEventFilter(self)

    @Slot()
    def iniciar_tarefa(self):
        """Inicia uma execução e impede tarefas simultâneas nesta demonstração."""
        if self.worker is not None:
            return

        self.cancelamento_solicitado = False
        self.window.concurrencyProgressBar.setValue(0)
        self.window.concurrencyStatusLabel.setText("Iniciando tarefa...")
        self.window.concurrencyStartButton.setEnabled(False)
        self.window.concurrencyCancelButton.setEnabled(True)

        # A duração é lida ao iniciar: mudar a preferência não altera uma
        # tarefa que já está em execução.
        duracao = (
            self.settings_service.carregar()["duracao"]
            if self.settings_service is not None else 20
        )
        self.worker = TaskWorker(self, duracao)
        # Como o controller é um QObject da thread principal, o Qt entrega
        # os sinais da tarefa aos slots desta thread. Widgets são atualizados
        # aqui, nunca dentro de run().
        self.worker.progresso.connect(self.atualizar_progresso)
        self.worker.finished.connect(self.finalizar_tarefa)
        self.worker.start()

    @Slot(int)
    def atualizar_progresso(self, percentual):
        # Sinais emitidos antes do pedido podem ainda estar na fila do Qt.
        # Não deixamos essas atualizações substituir a mensagem de cancelamento.
        if self.cancelamento_solicitado:
            return
        self.window.concurrencyProgressBar.setValue(percentual)
        self.window.concurrencyStatusLabel.setText(
            f"Tarefa em andamento: {percentual}% concluído."
        )

    @Slot()
    def cancelar_tarefa(self):
        """Solicita a parada sem bloquear o loop de eventos da interface."""
        if self.worker is None or not self.worker.isRunning():
            return

        self.cancelamento_solicitado = True
        self.window.concurrencyCancelButton.setEnabled(False)
        self.window.concurrencyStatusLabel.setText("Cancelando tarefa...")
        # O pedido não força a destruição da thread. O serviço consulta
        # a interrupção entre etapas e termina por conta própria.
        self.worker.requestInterruption()

    @Slot()
    def finalizar_tarefa(self):
        """Libera a tarefa encerrada e permite uma nova demonstração."""
        mensagem = (
            "Tarefa cancelada."
            if self.cancelamento_solicitado
            else "Tarefa concluída!"
        )
        self.window.concurrencyStatusLabel.setText(mensagem)
        self.window.concurrencyStartButton.setEnabled(True)
        self.window.concurrencyCancelButton.setEnabled(False)
        self.worker.deleteLater()
        self.worker = None

    def eventFilter(self, objeto, evento):
        if objeto is self.window and evento.type() == QEvent.Type.Close:
            if self.worker is not None:
                # A interrupção é cooperativa: run() consulta o pedido e sai.
                # wait() aguarda o término antes da destruição da janela.
                # Nesta simulação, a espera restante é de até uma etapa (100 ms).
                self.worker.requestInterruption()
                self.worker.wait()

            # Não precisamos observar outros eventos depois do fechamento.
            self.window.removeEventFilter(self)

        return super().eventFilter(objeto, evento)

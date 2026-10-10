from pathlib import Path

from PySide6.QtCore import QFile
from PySide6.QtGui import QColor, QPalette
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication, QFileDialog, QMessageBox, QPushButton


class SettingsController:
    """Aplica preferências à interface e abre a janela Sobre."""

    def __init__(self, window, service):
        self.window = window
        self.service = service
        self.package_dir = Path(__file__).resolve().parents[1]
        self.apresentar_preferencias()

        self.window.settingsThemeComboBox.currentTextChanged.connect(self.alterar_tema)
        self.window.settingsFontSizeSpinBox.valueChanged.connect(self.alterar_fonte)
        self.window.settingsTaskDurationSpinBox.valueChanged.connect(self.alterar_duracao)
        self.window.settingsDatabasePathInput.editingFinished.connect(self.alterar_banco)
        self.window.settingsBrowseDatabaseButton.clicked.connect(self.escolher_banco)
        self.window.settingsRestoreButton.clicked.connect(self.restaurar)
        self.window.settingsAboutButton.clicked.connect(self.abrir_sobre)

    def apresentar_preferencias(self):
        preferencias = self.service.carregar()
        campos = (
            self.window.settingsThemeComboBox,
            self.window.settingsFontSizeSpinBox,
            self.window.settingsTaskDurationSpinBox,
            self.window.settingsDatabasePathInput,
        )
        # Preencher os campos não deve disparar gravações ou mensagens.
        for campo in campos:
            campo.blockSignals(True)
        self.window.settingsThemeComboBox.setCurrentText(
            "Escuro" if preferencias["tema"] == "escuro" else "Claro"
        )
        self.window.settingsFontSizeSpinBox.setValue(preferencias["fonte"])
        self.window.settingsTaskDurationSpinBox.setValue(preferencias["duracao"])
        self.window.settingsDatabasePathInput.setText(preferencias["banco"])
        for campo in campos:
            campo.blockSignals(False)
        try:
            self.aplicar_tema(preferencias["tema"])
            self.aplicar_fonte(preferencias["fonte"])
            self.window.settingsStatusLabel.setText("Preferências carregadas.")
        except OSError as erro:
            self.window.settingsStatusLabel.setText(f"Erro ao carregar tema: {erro}")

    def salvar(self, chave, valor, mensagem="Preferência salva."):
        try:
            self.service.salvar(chave, valor)
            self.window.settingsStatusLabel.setText(mensagem)
        except OSError as erro:
            self.window.settingsStatusLabel.setText(str(erro))

    def aplicar_tema(self, tema):
        arquivo = "dark.qss" if tema == "escuro" else "light.qss"
        qss = (self.package_dir / "styles" / arquivo).read_text(encoding="utf-8")
        # URLs de imagens em QSS devem funcionar independentemente da pasta
        # de onde o usuário iniciou a aplicação.
        qss = qss.replace("@ASSET_DIR@", (self.package_dir / "styles").as_posix())
        app = QApplication.instance()
        # QSS cuida dos widgets. A paleta também fornece cores ao desenho
        # personalizado do CodeEditor, inclusive o destaque da linha atual.
        paleta = QPalette(app.style().standardPalette())
        cores = (
            ("#20242b", "#f1f3f5", "#171b21", "#303844", "#3b82f6")
            if tema == "escuro"
            else ("#dce3eb", "#18212c", "#edf1f5", "#cbd6e3", "#2563eb")
        )
        for papel, cor in zip(
            (QPalette.Window, QPalette.WindowText, QPalette.Base,
             QPalette.AlternateBase, QPalette.Highlight), cores
        ):
            paleta.setColor(papel, QColor(cor))
        for papel in (QPalette.Text, QPalette.ButtonText):
            paleta.setColor(papel, QColor(cores[1]))
        paleta.setColor(QPalette.HighlightedText, QColor("#ffffff"))
        paleta.setColor(QPalette.Button, QColor(cores[3]))
        app.setPalette(paleta)
        app.setStyleSheet(qss)
        # O QSS modifica o tamanho sugerido dos botões. Reservamos a largura
        # do texto completo, permitindo que o layout expanda sem cortá-lo.
        for button in self.window.navigationWidget.findChildren(QPushButton):
            button.setMinimumWidth(button.sizeHint().width())
        for editor in (self.window.codeEditor, self.window.dbSqlInput):
            editor.highlight_current_line()
            editor.line_number_area.update()

    def alterar_tema(self, texto):
        tema = "escuro" if texto == "Escuro" else "claro"
        try:
            self.aplicar_tema(tema)
        except OSError as erro:
            self.window.settingsStatusLabel.setText(f"Erro ao aplicar tema: {erro}")
            return
        self.salvar("tema", tema)

    def aplicar_fonte(self, tamanho):
        for editor in (self.window.codeEditor, self.window.dbSqlInput):
            fonte = editor.font()
            fonte.setPointSize(tamanho)
            editor.setFont(fonte)
            editor.line_number_area.update()

    def alterar_fonte(self, tamanho):
        self.aplicar_fonte(tamanho)
        self.salvar("fonte", tamanho)

    def alterar_duracao(self, segundos):
        self.salvar("duracao", segundos, "Duração salva para a próxima tarefa.")

    def alterar_banco(self):
        caminho = self.window.settingsDatabasePathInput.text().strip()
        if not caminho or not Path(caminho).is_absolute():
            self.window.settingsStatusLabel.setText("Informe um caminho absoluto para o banco.")
            return
        self.salvar("banco", caminho, "Banco padrão salvo para a próxima inicialização.")

    def escolher_banco(self):
        # O diálogo escolhe o caminho; não cria nem substitui um banco aqui.
        caminho, _ = QFileDialog.getSaveFileName(
            self.window, "Escolher banco padrão",
            self.window.settingsDatabasePathInput.text(),
            "Banco SQLite (*.db);;Todos os arquivos (*)",
            options=QFileDialog.Option.DontConfirmOverwrite,
        )
        if caminho:
            self.window.settingsDatabasePathInput.setText(caminho)
            self.alterar_banco()

    def restaurar(self):
        resposta = QMessageBox.question(
            self.window, "Restaurar padrões",
            "Deseja restaurar as preferências iniciais?\n"
            "O banco padrão será utilizado na próxima inicialização.",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No,
        )
        if resposta != QMessageBox.Yes:
            return
        try:
            self.service.restaurar()
        except OSError as erro:
            self.window.settingsStatusLabel.setText(str(erro))
            return
        self.apresentar_preferencias()
        self.window.settingsStatusLabel.setText("Padrões restaurados.")

    def abrir_sobre(self):
        arquivo = QFile(str(self.package_dir / "ui" / "about_dialog.ui"))
        if not arquivo.open(QFile.ReadOnly):
            self.window.settingsStatusLabel.setText("Não foi possível abrir a janela Sobre.")
            return
        loader = QUiLoader()
        dialogo = loader.load(arquivo, self.window)
        arquivo.close()
        if dialogo is None:
            self.window.settingsStatusLabel.setText(loader.errorString())
            return
        # exec() abre um diálogo modal: a janela principal aguarda sua resposta.
        dialogo.exec()
        dialogo.deleteLater()

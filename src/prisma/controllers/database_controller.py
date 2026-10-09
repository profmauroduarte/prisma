from prisma.services.database.sqlite_service import SQLiteService
from prisma.services.database.database_paths import caminho_banco_padrao
from PySide6.QtWidgets import QTableWidgetItem

class DatabaseController:
    """
    Controla a página DB Lab do PRISMA.
    """

    def __init__(self, window):
        self.window = window
        self.database = SQLiteService()

        # Apresenta o caminho padrão do banco na interface.
        self.window.dbPathInput.setText(
            str(caminho_banco_padrao())
        )

        self.window.dbStatusLabel.setText("Desconectado")

        self.window.dbConnectButton.clicked.connect(
            self.conectar_banco
        )

        self.window.dbExecuteButton.clicked.connect(
        self.executar_sql
)

    def conectar_banco(self):
        caminho = self.window.dbPathInput.text().strip()

        if not caminho:
            self.window.dbStatusLabel.setText(
                "Informe o caminho do banco de dados."
            )
            return

        try:
            self.database.conectar(caminho)

            self.window.dbStatusLabel.setText(
                "Conectado"
            )

        except Exception as erro:
            self.window.dbStatusLabel.setText(
                f"Erro na conexão: {erro}"
            )

    def executar_sql(self):
        """
        Executa o comando SQL digitado no DB Lab.
        """
        sql = self.window.dbSqlInput.toPlainText().strip()

        if not sql:
            self.window.dbSqlStatusLabel.setText(
                "Digite um comando SQL."
            )
            return

        try:
            colunas, registros, quantidade = self.database.executar(sql)

            self.exibir_resultados(colunas, registros)

            if colunas:
                mensagem = (
                    f"Consulta realizada: {quantidade} registro(s) encontrado(s)."
                )
            elif quantidade >= 0:
                mensagem = (
                    f"Comando executado: {quantidade} linha(s) afetada(s)."
                )
            else:
                mensagem = "Comando SQL executado com sucesso."

            self.window.dbSqlStatusLabel.setText(mensagem)

        except Exception as erro:
            self.window.dbSqlStatusLabel.setText(
                f"Erro SQL: {erro}"
            )

    def exibir_resultados(self, colunas, registros):
        """
        Exibe os resultados de uma consulta SQL na tabela.
        """
        tabela = self.window.dbResultsTable

        tabela.clear()

        tabela.setColumnCount(len(colunas))
        tabela.setRowCount(len(registros))

        tabela.setHorizontalHeaderLabels(colunas)

        for linha, registro in enumerate(registros):
            for coluna, valor in enumerate(registro):
                item = QTableWidgetItem(
                    "NULL" if valor is None else str(valor)
                )

                tabela.setItem(linha, coluna, item)

        tabela.resizeColumnsToContents()
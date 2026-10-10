from prisma.services.database.sqlite_service import SQLiteService
from prisma.services.database.database_paths import caminho_banco_padrao
from PySide6.QtWidgets import QTableWidgetItem

class DatabaseController:
    """
    Controla a página DB Lab do PRISMA.
    """

    def __init__(self, window, settings_service=None):
        self.window = window
        # O controller conhece a interface; o serviço conhece o SQLite.
        # Essa divisão permite usar o serviço sem abrir uma janela.
        self.database = SQLiteService()

        # Apresenta o caminho padrão do banco na interface.
        self.window.dbPathInput.setText(
            settings_service.carregar()["banco"]
            if settings_service is not None else str(caminho_banco_padrao())
        )

        self.window.dbStatusLabel.setText("Desconectado")

        # connect() registra o método que será chamado quando o botão emitir
        # o sinal clicked; o método não é executado durante esta configuração.
        self.window.dbConnectButton.clicked.connect(
            self.conectar_banco
        )

        self.window.dbExecuteButton.clicked.connect(
        self.executar_sql
)

    def conectar_banco(self):
        # strip() remove espaços nas extremidades antes de validar o campo.
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
            # Desempacota os três valores retornados pelo serviço: estrutura
            # das colunas, conteúdo das linhas e contagem para a mensagem.
            colunas, registros, quantidade = self.database.executar(sql)

            self.exibir_resultados(colunas, registros)

            if colunas:
                mensagem = (
                    f"Consulta realizada: {quantidade} registro(s) encontrado(s)."
                )
            # Uma contagem negativa indica que o comando não fornece quantidade
            # de linhas afetadas; nesse caso, usamos uma mensagem sem contagem.
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

        # Remove células e cabeçalhos da consulta anterior. As dimensões
        # são ajustadas em seguida, inclusive quando o resultado está vazio.
        tabela.clear()

        tabela.setColumnCount(len(colunas))
        tabela.setRowCount(len(registros))

        tabela.setHorizontalHeaderLabels(colunas)

        # enumerate() fornece o índice e o conteúdo. Os índices da tabela
        # começam em zero, assim como os índices das sequências Python.
        for linha, registro in enumerate(registros):
            for coluna, valor in enumerate(registro):
                # Cada célula recebe um item próprio. None representa NULL no SQL;
                # os demais valores são convertidos em texto para exibição.
                item = QTableWidgetItem(
                    "NULL" if valor is None else str(valor)
                )

                tabela.setItem(linha, coluna, item)

        tabela.resizeColumnsToContents()

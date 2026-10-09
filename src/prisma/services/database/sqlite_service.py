import sqlite3


class SQLiteService:
    """
    Gerencia a conexão com um banco de dados SQLite.

    A interface gráfica não acessa o banco diretamente.
    Essa responsabilidade pertence ao serviço.
    """

    def __init__(self):
        self.conexao = None

    def conectar(self, caminho):
        """
        Abre um banco SQLite existente ou cria um novo arquivo.
        """
        if self.conexao is not None:
            self.desconectar()

        self.conexao = sqlite3.connect(caminho)

    def desconectar(self):
        """
        Fecha a conexão com o banco de dados.
        """
        if self.conexao is not None:
            self.conexao.close()
            self.conexao = None

    def executar(self, sql):
        """
        Executa um comando SQL e retorna os resultados.

        Para consultas, retorna os nomes das colunas e os registros.
        Para outros comandos, confirma as alterações no banco.
        """
        if self.conexao is None:
            raise RuntimeError(
                "Nenhum banco de dados conectado."
            )

        cursor = self.conexao.cursor()
        cursor.execute(sql)

        if cursor.description is not None:
            colunas = [
                coluna[0] for coluna in cursor.description
            ]
            registros = cursor.fetchall()

            return colunas, registros, len(registros)

        linhas_afetadas = cursor.rowcount

        self.conexao.commit()

        return [], [], linhas_afetadas
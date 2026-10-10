import sqlite3


class SQLiteService:
    """
    Gerencia a conexão com um banco de dados SQLite.

    A interface gráfica não acessa o banco diretamente.
    Essa responsabilidade pertence ao serviço.
    """

    def __init__(self):
        # None representa a ausência de conexão; a mesma conexão será usada
        # pelos comandos seguintes até ser fechada ou substituída.
        self.conexao = None

    def conectar(self, caminho):
        """
        Abre um banco SQLite existente ou cria um novo arquivo.
        """
        # Ao trocar de banco, fecha a conexão anterior antes de abrir outra.
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

        # O cursor executa o comando e permite acessar seus resultados.
        # execute() recebe um comando por chamada, não um script com vários comandos.
        cursor = self.conexao.cursor()
        cursor.execute(sql)

        # description contém metadados das colunas quando o comando produz
        # um resultado, mesmo que a consulta não encontre nenhum registro.
        if cursor.description is not None:
            # Cada descrição de coluna é uma sequência; o primeiro item é seu nome.
            colunas = [
                coluna[0] for coluna in cursor.description
            ]
            # fetchall() reúne as linhas restantes como tuplas de valores.
            # O controller recebe dados Python, sem depender de widgets do Qt.
            registros = cursor.fetchall()

            return colunas, registros, len(registros)

        # rowcount informa as linhas afetadas por alterações. Para comandos
        # como CREATE TABLE, o SQLite pode retornar -1 (contagem indisponível).
        linhas_afetadas = cursor.rowcount

        # commit() confirma as alterações da transação para persistir no banco.
        self.conexao.commit()

        return [], [], linhas_afetadas
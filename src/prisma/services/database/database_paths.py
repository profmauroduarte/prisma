from pathlib import Path

from PySide6.QtCore import QStandardPaths


def diretorio_bancos():
    """
    Retorna o diretório onde o PRISMA armazena
    seus bancos de dados SQLite.
    """
    # O Qt escolhe o diretório de dados adequado ao sistema operacional
    # e ao nome definido por QApplication.setApplicationName().
    # Path facilita compor caminhos sem fixar separadores como / ou \.
    diretorio = Path(
        QStandardPaths.writableLocation(
            QStandardPaths.AppLocalDataLocation
        )
    )

    # parents=True cria também os diretórios intermediários.
    # exist_ok=True permite reutilizar uma pasta já existente.
    diretorio.mkdir(
        parents=True,
        exist_ok=True,
    )

    return diretorio


def caminho_banco_padrao():
    """
    Retorna o caminho completo do banco padrão.
    """
    return diretorio_bancos() / "laboratorio.db"
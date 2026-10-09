from pathlib import Path

from PySide6.QtCore import QStandardPaths


def diretorio_bancos():
    """
    Retorna o diretório onde o PRISMA armazena
    seus bancos de dados SQLite.
    """
    diretorio = Path(
        QStandardPaths.writableLocation(
            QStandardPaths.AppLocalDataLocation
        )
    )

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
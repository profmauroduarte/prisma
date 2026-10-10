from PySide6.QtCore import QSettings

from prisma.services.database.database_paths import caminho_banco_padrao


class SettingsService:
    """Persiste preferências do usuário, sem conhecer os widgets."""

    def __init__(self, settings=None):
        # Organização e aplicação identificam o armazenamento no sistema.
        # Uma instância pode ser fornecida para testes com arquivo temporário.
        self.settings = settings if settings is not None else QSettings("PRISMA", "PRISMA")
        self.padroes = {
            "tema": "claro",
            "fonte": 12,
            "duracao": 20,
            "banco": str(caminho_banco_padrao()),
        }

    def carregar(self):
        preferencias = {}
        for chave, padrao in self.padroes.items():
            valor = self.settings.value(chave, padrao)
            # Preferências antigas ou editadas manualmente não devem impedir
            # a abertura da aplicação. Valores inválidos usam o padrão.
            if chave in ("fonte", "duracao"):
                try:
                    valor = int(valor)
                except (TypeError, ValueError):
                    valor = padrao
                minimo, maximo = (8, 24) if chave == "fonte" else (5, 30)
                if not minimo <= valor <= maximo:
                    valor = padrao
            elif chave == "tema":
                if valor not in ("claro", "escuro"):
                    valor = padrao
            elif not isinstance(valor, str) or not valor.strip():
                valor = padrao
            preferencias[chave] = valor
        return preferencias

    def salvar(self, chave, valor):
        self.settings.setValue(chave, valor)
        # sync() solicita a gravação e permite detectar falhas de persistência.
        self.settings.sync()
        if self.settings.status() != QSettings.Status.NoError:
            raise OSError("Não foi possível salvar as preferências.")

    def restaurar(self):
        # Remove apenas as preferências conhecidas, preservando futuras chaves.
        for chave in self.padroes:
            self.settings.remove(chave)
        self.settings.sync()
        if self.settings.status() != QSettings.Status.NoError:
            raise OSError("Não foi possível restaurar as preferências.")

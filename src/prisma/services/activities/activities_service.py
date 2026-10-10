import json
from pathlib import Path


class ActivitiesService:
    """Fornece um catálogo de atividades sem depender da interface gráfica."""

    MODULOS = ("playground", "database", "api")
    CAMPOS = ("id", "modulo", "titulo", "objetivo", "instrucoes", "resultado_esperado")

    def carregar(self):
        # O catálogo acompanha o pacote. No futuro, a obtenção dos dados
        # poderá usar uma API, preservando o formato consumido pela tela.
        caminho = Path(__file__).resolve().parents[2] / "resources" / "activities.json"
        with caminho.open(encoding="utf-8") as arquivo:
            atividades = json.load(arquivo)

        # Valida antes de devolver os dados para evitar uma lista parcialmente
        # carregada quando houver um cadastro incompleto ou malformado.
        if not isinstance(atividades, list):
            raise ValueError("O catálogo deve conter uma lista de atividades.")

        identificadores = set()
        for atividade in atividades:
            if not isinstance(atividade, dict) or any(
                not isinstance(atividade.get(campo), str)
                or not atividade[campo].strip()
                for campo in self.CAMPOS
            ):
                raise ValueError("Cada atividade deve conter todos os campos de texto obrigatórios.")
            if atividade["modulo"] not in self.MODULOS:
                raise ValueError("O catálogo contém um módulo desconhecido.")
            if atividade["id"] in identificadores:
                raise ValueError("O catálogo contém identificadores repetidos.")
            identificadores.add(atividade["id"])

        return atividades

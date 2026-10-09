# ============================================================
# PRISMA — Playground de Lógica
#
# Arquivo: error_messages.py
#
# Responsabilidade:
#   - associar os tipos de erro do Python a mensagens amigáveis;
#   - fornecer explicações para o console do Playground.
# ============================================================

# As chaves correspondem ao nome do tipo da exceção capturada pelo CodeRunner.
ERROR_MESSAGES = {
    "SyntaxError": "Erro de sintaxe",
    "NameError": "Variável ou nome não definido",
    "TypeError": "Tipo de dado inválido",
    "ValueError": "Valor inválido",
    "ZeroDivisionError": "Divisão por zero",
    "IndexError": "Índice fora do limite",
    "KeyError": "Chave não encontrada",
    "IndentationError": "Erro de indentação",
    "TabError": "Uso inconsistente de espaços e tabulações na indentação",
    "AttributeError": "Objeto não possui esse atributo",
    "ImportError": "Não foi possível importar o módulo ou recurso",
    "ModuleNotFoundError": "Módulo não encontrado",
    "FileNotFoundError": "Arquivo não encontrado",
    "OverflowError": "Resultado grande demais",
    "AssertionError": "Falha em uma afirmação",
    "EOFError": "Fim inesperado da entrada",
}
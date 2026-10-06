# QPlainTextEdit é o editor de texto que vamos personalizar.
# QWidget será usado para criar a área lateral dos números.
from PySide6.QtWidgets import QPlainTextEdit, QWidget, QTextEdit

# QPainter é responsável por desenhar os números das linhas.
# QTextFormat é usado para obter o formato do texto.
from PySide6.QtGui import QPainter, QTextFormat


# Qt fornece constantes utilizadas durante o desenho,
# como o alinhamento do texto.
from PySide6.QtCore import Qt


# -------------------------------------------------------------------
# ÁREA DOS NÚMEROS DAS LINHAS
# -------------------------------------------------------------------
#
# Esta classe representa a pequena área lateral que fica à esquerda
# do editor e onde os números das linhas são desenhados.
#
# Ela pertence ao CodeEditor e utiliza o próprio editor para descobrir
# quais linhas estão visíveis.
class LineNumberArea(QWidget):

    def __init__(self, editor):
        # O editor será o "pai" deste widget.
        # Isso faz com que a área acompanhe o CodeEditor.
        super().__init__(editor)

        # Guardamos uma referência ao editor para poder utilizá-lo
        # durante o desenho dos números.
        self.editor = editor

    def paintEvent(self, event):
        # QPainter é a ferramenta do Qt usada para desenhar
        # diretamente na área dos números.
        painter = QPainter(self)

        # Pedimos ao CodeEditor que faça o desenho dos números.
        self.editor.paint_line_numbers(painter, event)


# -------------------------------------------------------------------
# EDITOR DE CÓDIGO
# -------------------------------------------------------------------
#
# Nossa classe herda de QPlainTextEdit.
#
# Isso significa que continuamos utilizando o editor padrão do Qt,
# mas podemos adicionar comportamentos próprios, como a numeração
# das linhas.
class CodeEditor(QPlainTextEdit):

    def __init__(self, parent=None):
        # Inicializa o QPlainTextEdit original.
        #
        # O parâmetro parent é importante porque o QUiLoader pode
        # fornecê-lo automaticamente quando cria este componente
        # a partir do arquivo .ui.
        super().__init__(parent)

        # Cria a área lateral onde os números das linhas serão
        # desenhados.
        self.line_number_area = LineNumberArea(self)

        # Este sinal é emitido quando a quantidade de blocos de texto
        # muda. Na prática, usamos isso para recalcular o espaço
        # necessário para os números das linhas.
        self.blockCountChanged.connect(
            self.update_line_number_area_width
        )

        # Este sinal é emitido quando a área visível do editor
        # precisa ser atualizada, por exemplo durante a rolagem.
        #
        # Precisamos atualizar também a área dos números para que
        # ela acompanhe o texto.
        self.updateRequest.connect(
            self.update_line_number_area
        )
        # Este sinal é emitido quando o cursor do editor muda de posição.
        # Precisamos disso para destacar a linha atual, mas também
        self.cursorPositionChanged.connect(
            self.highlight_current_line
        )

        # Define inicialmente o espaço reservado para os números.
        self.update_line_number_area_width(0)
        self.highlight_current_line()

    # ----------------------------------------------------------------
    # DEFINE O ESPAÇO RESERVADO PARA OS NÚMEROS
    # ----------------------------------------------------------------
    def update_line_number_area_width(self, _):
        # Reserva 40 pixels no lado esquerdo do editor.
        #
        # Os outros três valores representam:
        # esquerda, superior, direita e inferior.
        self.setViewportMargins(40, 0, 0, 0)

    # ----------------------------------------------------------------
    # ATUALIZA A ÁREA DOS NÚMEROS
    # ----------------------------------------------------------------
    def update_line_number_area(self, rect, dy):

        # Se o conteúdo foi deslocado verticalmente, deslocamos
        # também a área dos números na mesma quantidade.
        if dy:
            self.line_number_area.scroll(0, dy)

        # Caso contrário, solicitamos que a área seja redesenhada
        # apenas na região que precisa ser atualizada.
        else:
            self.line_number_area.update(
                0,
                rect.y(),
                self.line_number_area.width(),
                rect.height()
            )

        # Se a região atualizada corresponde à área visível inteira,
        # recalculamos o espaço reservado para os números.
        if rect.contains(self.viewport().rect()):
            self.update_line_number_area_width(0)

    # ----------------------------------------------------------------
    # AJUSTA A POSIÇÃO DA ÁREA DOS NÚMEROS
    # ----------------------------------------------------------------
    def resizeEvent(self, event):

        # Primeiro deixamos o QPlainTextEdit tratar normalmente
        # o redimensionamento.
        super().resizeEvent(event)

        # Obtém o tamanho atual do editor.
        rect = self.contentsRect()

        # Posiciona a área dos números no lado esquerdo do editor.
        #
        # Os valores representam:
        # x, y, largura e altura.
        self.line_number_area.setGeometry(
            rect.left(),
            rect.top(),
            40,
            rect.height()
        )

    # ----------------------------------------------------------------
    # DESENHA OS NÚMEROS DAS LINHAS
    # ----------------------------------------------------------------
    def paint_line_numbers(self, painter, event):

        # Obtém o primeiro bloco de texto que está atualmente visível.
        #
        # No QPlainTextEdit, cada linha de texto é tratada como
        # um bloco.
        block = self.firstVisibleBlock()

        # Obtém o número desse bloco.
        #
        # O Qt começa a contagem em 0, por isso posteriormente
        # adicionamos 1 para mostrar ao usuário.
        block_number = block.blockNumber()

        # Calcula a posição vertical da primeira linha visível.
        top = self.blockBoundingGeometry(block).translated(
            self.contentOffset()
        ).top()

        # Calcula onde termina essa primeira linha.
        bottom = (
            top
            + self.blockBoundingRect(block).height()
        )

        # Continua percorrendo as linhas enquanto elas estiverem
        # dentro da área visível do editor.
        while block.isValid() and top <= event.rect().bottom():

            # Só desenhamos linhas que realmente estão visíveis
            # dentro da área que está sendo atualizada.
            if block.isVisible() and bottom >= event.rect().top():

                # Converte o número da linha para texto.
                #
                # Como o Qt começa em 0, adicionamos 1.
                number = str(block_number + 1)

                # Desenha o número da linha.
                #
                # O número fica alinhado à direita dentro da
                # área lateral.
                painter.drawText(
                    0,
                    int(top),
                    self.line_number_area.width() - 5,
                    int(self.fontMetrics().height()),
                    Qt.AlignRight,
                    number
                )

            # Passa para o próximo bloco/linha.
            block = block.next()

            # A próxima linha começa onde terminou a atual.
            top = bottom

            # Calcula a posição inferior da próxima linha.
            bottom = (
                top
                + self.blockBoundingRect(block).height()
            )

            # Avança o contador da linha.
            block_number += 1
#   #   ----------------------------------------------------------------
#   # DESTAQUE DA LINHA ATUAL
#   # ---------------------------------------------------------------- 
    def highlight_current_line(self):
        extra_selection = []

        selection = QTextEdit.ExtraSelection()
        
        selection.format.setBackground(
            self.palette().alternateBase()
        )

        selection.format.setProperty(
            QTextFormat.FullWidthSelection,
            True
        )

        selection.cursor = self.textCursor()
        selection.cursor.clearSelection()

        extra_selection.append(selection)

        self.setExtraSelections(extra_selection)
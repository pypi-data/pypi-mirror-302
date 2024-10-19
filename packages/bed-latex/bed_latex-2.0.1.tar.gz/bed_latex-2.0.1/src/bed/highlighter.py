"""
Copyright 2015-2024 Jean-Baptiste Delisle

This file is part of BEd.

BEd is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

BEd is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with BEd.  If not, see <http://www.gnu.org/licenses/>.
"""

# This file defines the BedHighlighter class that allows BedWidgets (see editor.py)
# to highlight TeX commands. It requires the pygments library.
from PySide6 import QtGui

# Syntax highlighting (if available)
try:
  from pygments import highlight as pygments_highlight
  from pygments.formatter import Formatter as pygments_Formatter
  from pygments.lexers import TexLexer as pygments_TexLexer

  pygments_available = True
except ImportError:
  pygments_available = False

# Check if pygments is available (otherwise do nothing)
if pygments_available:

  class QtFormatter(pygments_Formatter):
    """Class that implement a pygments formatter for Qt.
    This code is based on tutorial at:
    http://pygments.org/docs/formatterdevelopment
    """

    def __init__(self, **options):
      super().__init__(**options)
      # create a dict of Qt text styles (QtGui.QTextCharFormat)
      self.styles = {}
      # we iterate over the `_styles` attribute of a style item
      # that contains the parsed style values.
      for token, style in self.style:
        qtstyle = QtGui.QTextCharFormat()
        if style['color']:
          qtstyle.setForeground(self.hex2QColor(style['color']))
        if style['bgcolor']:
          qtstyle.setBackground(self.hex2QColor(style['bgcolor']))
        if style['bold']:
          qtstyle.setFontWeight(QtGui.QFont.Bold)
        if style['italic']:
          qtstyle.setFontItalic(True)
        if style['underline']:
          qtstyle.setFontUnderline(True)
        self.styles[token] = qtstyle
      # init output lists
      # (we want the output to stay a python object,
      #  and not to be written in a text file as normally done by pygments)
      # self.out_styles is the list of styles to be applied to the text
      # self.out_indexes is the list of starting char indexes in the text
      # that delimits where to apply the styles
      self.out_styles = []
      self.out_indexes = []

    def format(self, tokensource, outfile):
      # outfile is ignored
      # the output is provided in the self.output list
      self.out_styles = []
      self.out_indexes = []
      # lasttype is used for caching
      # because it's possible that an lexer yields a number
      # of consecutive tokens with the same token type.
      # to minimize the size of the output
      current_index = 0
      lasttype = None
      for ttype, value in tokensource:
        # if the token type doesn't exist in the stylemap
        # we try it with the parent of the token type
        # eg: parent of Token.Literal.String.Double is
        # Token.Literal.String
        while ttype not in self.styles:
          ttype = ttype.parent
        if ttype != lasttype:
          if current_index > 0:
            self.out_styles.append(self.styles[lasttype])
            self.out_indexes.append(current_index)
          lasttype = ttype
        current_index += len(value)
      if current_index > 0:
        self.out_styles.append(self.styles[lasttype])
        self.out_indexes.append(current_index)

    def hex2QColor(self, hexcode):
      """Translate hexadecimal color code to Qt QColor"""
      R = int(hexcode[0:2], 16)
      G = int(hexcode[2:4], 16)
      B = int(hexcode[4:6], 16)
      return QtGui.QColor(R, G, B)

  class BedHighlighter(QtGui.QSyntaxHighlighter):
    """This class implement a TeX syntax highlighter that calls pygments
    to do the job.
    """

    def __init__(self, parent):
      super().__init__(parent)
      # Init pygments formatter and lexer
      self.formatter = QtFormatter()
      self.lexer = pygments_TexLexer()

    def highlightBlock(self, text):
      """Highlight a block of text"""
      # Ignore text and get the whole text
      # (to let pygments decide with the full context)
      # (not very efficient, but seems fast enough)
      whole_text = self.document().toPlainText() + '\n'
      pygments_highlight(whole_text, self.lexer, self.formatter)
      # Find position and length of the block to be highlighted
      current_block = self.currentBlock()
      blockstart = current_block.position()
      blockend = blockstart + current_block.length()
      # Only apply the format to the current block
      start_index = blockstart
      for end_index, qtstyle in zip(
        self.formatter.out_indexes, self.formatter.out_styles
      ):
        # If end_index < blockstart, just pass (the block has not yet been reached)
        if end_index > blockstart:
          # If end_index >= blockend, end of block has been reached
          # apply style to the end of the block and break loop
          if end_index >= blockend:
            # relative position in the block and length
            self.setFormat(start_index - blockstart, blockend - start_index, qtstyle)
            break
          # relative position in the block and length
          self.setFormat(start_index - blockstart, end_index - start_index, qtstyle)
        # set value of start_index for next iteration
        start_index = max(end_index, blockstart)

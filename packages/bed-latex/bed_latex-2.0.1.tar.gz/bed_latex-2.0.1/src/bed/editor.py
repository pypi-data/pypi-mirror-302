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

# This file defines the BEd properties editor (class PropertiesEditor).
# It is a simple QDialog with a FormLayout.
# Each line of the form is a property that can be edited (class BedWidget).
# A BedWidget is a QtWidget (QLineEdit, QSpinBox...) that has
# additionnal functions.
from PySide6 import QtCore, QtGui, QtWidgets

# Syntax highlighting (if available)
try:
  from .highlighter import BedHighlighter

  pygments_available = True
except ImportError:
  pygments_available = False


class AdjustTextEdit(QtWidgets.QTextEdit):
  """Class that inherits QTextEdit but with a minimum height adjusting to content"""

  def __init__(self, plainText='', parent=None):
    """Initialisation"""
    super().__init__(parent=parent)
    # Force the text to be plainText
    self.setAcceptRichText(False)
    self.setPlainText(plainText)

  def paintEvent(self, *args, **kwargs):
    """Painting"""
    # Get content size
    document_size = self.document().size().toSize()
    # Adjust minimum height to content
    self.setMinimumHeight(document_size.height() + 5)
    # Paint
    super().paintEvent(*args, **kwargs)


class ColorDialogButton(QtWidgets.QWidget):
  """Colored button that trigger a QColorDialog when clicked"""

  colorChanged = QtCore.Signal(QtGui.QColor, name='colorChanged')

  def __init__(self, color, parent=None):
    """Initialisation"""
    super().__init__(parent=parent)
    self.setMinimumSize(50, 25)
    self.setMaximumSize(50, 25)
    self.setColor(color)

  def setColor(self, color):
    """Change the button color and trigger colorChanged signal"""
    self.color = color
    self.repaint()
    self.colorChanged.emit(color)

  def paintEvent(self, *args, **kwargs):
    """Painting"""
    # Draw colored rectangle with gray border
    painter = QtGui.QPainter()
    painter.begin(self)
    painter.setBrush(self.color)
    painter.setPen(QtGui.QPen(QtGui.QColor('gray'), 1.0))
    painter.drawRect(QtCore.QRectF(0.5, 0.5, self.width() - 1, self.height() - 1))
    painter.end()

  def mouseReleaseEvent(self, event):
    """Launch QColorDialog when button is clicked"""
    color = QtWidgets.QColorDialog.getColor(initial=self.color, parent=self.parent())
    if color.isValid():
      self.setColor(color)


class BedWidget:
  """Class that contains one or several QtWidgets with additionnal functions"""

  def __init__(
    self, value, label=None, widgets=None, default=None, onChange=None, parent=None
  ):
    """Initialisation"""
    # Remember previous value
    self.prev_value = value
    # Label to be written in front of the widget in the form layout
    self.label = QtWidgets.QLabel(label) if label else None
    # Qt widgets embedded in the BedWidget
    self.widgets = widgets if widgets else []
    self.default = default
    if len(widgets) == 1 and default is None:
      self.container = widgets[0]
    else:
      self.container = QtWidgets.QWidget()
      layout = QtWidgets.QHBoxLayout(self.container)
      layout.setContentsMargins(0, 0, 0, 0)
      for widget in widgets:
        layout.addWidget(widget)
      if default is not None:
        self.resetbutton = QtWidgets.QPushButton(self.tr('Reset'))
        self.resetbutton.clicked.connect(self.resetValue)
        if value == default:
          self.resetbutton.setVisible(False)
        layout.addWidget(self.resetbutton)

    # Function to be called when the widget is modified
    self.onChange = onChange
    # Parent widget
    self.parent = parent

  def value(self):
    """Function that provide the value of the widget in a uniformed way"""
    return

  def setValue(self, value):
    """Function that set the value of the widget in a uniformed way"""

  def resetValue(self):
    self.setValue(self.default)
    self.resetbutton.setVisible(False)

  def onChangeConnect(self):
    """Connector that is raised when the widget is edited"""
    # Show/hide the reset button...
    if self.default is not None:
      if self.value() == self.default:
        self.resetbutton.setVisible(False)
      else:
        self.resetbutton.setVisible(True)
    # Call the onChange function if it is defined and needed
    if self.onChange and not self.parent.changing:
      self.onChange(self.parent)
    # Remember previous value
    self.prev_value = self.value()

  def tr(self, sourceText, disambiguation=''):
    return QtCore.QCoreApplication.translate('BedWidget', sourceText, disambiguation)


class BedLineEdit(BedWidget):
  """BedWidget containing a QLineEdit"""

  def __init__(
    self, value, label=None, default=None, onChange=None, highlight=False, parent=None
  ):
    """Initialisation"""
    super().__init__(
      value, label, [QtWidgets.QLineEdit(value)], default, onChange, parent
    )
    self.widgets[0].editingFinished.connect(self.onChangeConnect)
    if highlight and pygments_available:
      self.highlighter = BedHighlighter(self.widgets[0].document())

  def value(self):
    return self.widgets[0].text()

  def setValue(self, value):
    self.widgets[0].setText(value)
    self.prev_value = self.value()


class BedAdjustTextEdit(BedWidget):
  """BedWidget containing an AdjustTextEdit"""

  def __init__(
    self, value, label=None, default=None, onChange=None, highlight=False, parent=None
  ):
    """Initialisation"""
    super().__init__(
      value, label, [AdjustTextEdit(value, parent)], default, onChange, parent
    )
    self.widgets[0].textChanged.connect(self.onChangeConnect)
    if highlight and pygments_available:
      self.highlighter = BedHighlighter(self.widgets[0].document())

  def value(self):
    return self.widgets[0].toPlainText()

  def setValue(self, value):
    self.widgets[0].setPlainText(value)
    self.prev_value = self.value()


class BedSpinBox(BedWidget):
  """BedWidget containing a QSpinBox"""

  def __init__(
    self, value, mini, maxi, step, label=None, default=None, onChange=None, parent=None
  ):
    """Initialisation"""
    super().__init__(value, label, [QtWidgets.QSpinBox()], default, onChange, parent)
    self.widgets[0].setRange(mini, maxi)
    self.widgets[0].setSingleStep(step)
    self.widgets[0].setValue(value)
    self.widgets[0].editingFinished.connect(self.onChangeConnect)

  def value(self):
    return self.widgets[0].value()

  def setValue(self, value):
    self.widgets[0].setValue(value)
    self.prev_value = self.value()


class BedDoubleSpinBox(BedWidget):
  """BedWidget containing a QDoubleSpinBox"""

  def __init__(
    self,
    value,
    mini,
    maxi,
    step,
    decimals,
    label=None,
    default=None,
    onChange=None,
    parent=None,
  ):
    """Initialisation"""
    super().__init__(
      value, label, [QtWidgets.QDoubleSpinBox()], default, onChange, parent
    )
    self.widgets[0].setRange(mini, maxi)
    self.widgets[0].setSingleStep(step)
    self.widgets[0].setDecimals(decimals)
    self.widgets[0].setValue(value)
    self.widgets[0].editingFinished.connect(self.onChangeConnect)

  def value(self):
    return self.widgets[0].value()

  def setValue(self, value):
    self.widgets[0].setValue(value)
    self.prev_value = self.value()


class BedCheckBox(BedWidget):
  """BedWidget containing a QCheckBox"""

  def __init__(
    self, value, label=None, checklabel=None, default=None, onChange=None, parent=None
  ):
    """Initialisation"""
    super().__init__(
      value, label, [QtWidgets.QCheckBox(checklabel)], default, onChange, parent
    )
    self.widgets[0].setChecked(value)
    self.widgets[0].stateChanged.connect(self.onChangeConnect)

  def value(self):
    return self.widgets[0].checkState() == QtCore.Qt.Checked

  def setValue(self, value):
    self.widgets[0].setChecked(value)
    self.prev_value = self.value()


class BedComboBox(BedWidget):
  """BedWidget containing a QComboBox"""

  def __init__(
    self,
    value,
    listvals,
    label=None,
    checklabel=None,
    default=None,
    onChange=None,
    parent=None,
  ):
    """Initialisation"""
    super().__init__(value, label, [QtWidgets.QComboBox()], default, onChange, parent)
    self.widget = QtWidgets.QComboBox()
    self.widgets[0].addItems(listvals)
    self.widgets[0].setCurrentIndex(value)
    self.widgets[0].currentIndexChanged.connect(self.onChangeConnect)

  def value(self):
    return self.widgets[0].currentIndex()

  def setValue(self, value):
    self.widgets[0].setCurrentIndex(value)
    self.prev_value = self.value()


class BedColorPicker(BedWidget):
  """BedWidget containing a ColorDialogButton"""

  def __init__(self, value, label=None, default=None, onChange=None, parent=None):
    """Initialisation"""
    super().__init__(
      value, label, [ColorDialogButton(value, parent)], default, onChange, parent
    )
    self.widgets[0].colorChanged.connect(self.onChangeConnect)

  def value(self):
    return self.widgets[0].color

  def setValue(self, value):
    self.widgets[0].setColor(value)
    self.prev_value = self.value()


class BedPenPicker(BedWidget):
  """BedWidget containing a ColorDialogButton + QDoubleSpinBox"""

  def __init__(self, value, label=None, default=None, onChange=None, parent=None):
    """Initialisation"""
    super().__init__(
      value,
      label,
      [ColorDialogButton(value.color(), parent), QtWidgets.QDoubleSpinBox()],
      default,
      onChange,
      parent,
    )
    self.widgets[0].colorChanged.connect(self.onChangeConnect)
    self.widgets[1].setRange(0, 100)
    self.widgets[1].setSingleStep(0.1)
    self.widgets[1].setDecimals(2)
    self.widgets[1].setValue(value.widthF())
    self.widgets[1].editingFinished.connect(self.onChangeConnect)

  def value(self):
    return QtGui.QPen(self.widgets[0].color, self.widgets[1].value())

  def setValue(self, value):
    self.widgets[0].setColor(value.color())
    self.widgets[1].setValue(value.widthF())
    self.prev_value = self.value()


class BedPushButton(BedWidget):
  """BedWidget containing a QPushButton"""

  def __init__(self, label=None, buttonlabel=None, onChange=None, parent=None):
    """Initialisation"""
    super().__init__(
      None, label, [QtWidgets.QPushButton(buttonlabel)], None, onChange, parent
    )
    self.widgets[0].clicked.connect(self.onChangeConnect)


class PropertiesEditor(QtWidgets.QDialog):
  """Dialog that ask the user for changes in objects properties"""

  def __init__(self, parent, bedwidgets, settings, objtype, objname):
    """Initialisation"""
    super().__init__(parent)
    self.setWindowTitle(self.tr('BEd - Properties Editor') + ' (' + objname + ')')
    self.setMinimumSize(300, 300)
    self.resize(
      settings.__dict__['editor_' + objtype + '_width'],
      settings.__dict__['editor_' + objtype + '_height'],
    )
    self.bedwidgets = bedwidgets
    self.changing = False
    self.settings = settings
    self.objtype = objtype
    globlayout = QtWidgets.QVBoxLayout(self)
    # Scrollbar around form
    scroll = QtWidgets.QScrollArea(self)
    globlayout.addWidget(scroll)
    scroll.setWidgetResizable(True)
    view = QtWidgets.QWidget(scroll)
    scroll.setWidget(view)
    # Formlayout listing all properties
    proplayout = QtWidgets.QFormLayout(view)
    proplayout.setFieldGrowthPolicy(QtWidgets.QFormLayout.ExpandingFieldsGrow)
    view.setLayout(proplayout)
    # Loop over properties (BedWidgets)
    for bwid in bedwidgets:
      bwid.parent = self
      # Put a name in front of the widgets container if bwid.label is defined
      if bwid.label:
        proplayout.addRow(bwid.label, bwid.container)
      else:
        proplayout.addRow(bwid.container)

    # OK and Cancel buttons
    buttons = QtWidgets.QDialogButtonBox(
      QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel,
      QtCore.Qt.Horizontal,
      self,
    )
    globlayout.addWidget(buttons)

    # Connectors
    buttons.accepted.connect(self.accept)
    buttons.rejected.connect(self.reject)

  @staticmethod
  def getValues(parent, bedwidgets, settings, objtype, objname):
    """Static method that is called in the main file to get
    the final values of the paramaters (if they changed)
    """
    QtWidgets.QApplication.restoreOverrideCursor()
    dialog = PropertiesEditor(parent, bedwidgets, settings, objtype, objname)
    ok = dialog.exec_()
    if ok:
      # Return the list of parameters
      return [bwid.value() for bwid in dialog.bedwidgets]
    # Return None if the user canceled
    return None

  def resizeEvent(self, event):
    """Things to do when the user resize the window"""
    # Most important resizing consequences are treated by the painterArea resizeEvent
    # Here we just save the new size in the application settings
    self.settings.__dict__['editor_' + self.objtype + '_width'] = self.width()
    self.settings.__dict__['editor_' + self.objtype + '_height'] = self.height()

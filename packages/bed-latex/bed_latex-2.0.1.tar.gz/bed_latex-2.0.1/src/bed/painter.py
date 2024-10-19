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

# This file defines the PainterArea class,
# which deals with the drawings
# and the mouse events

import time

from PySide6 import QtCore, QtGui, QtWidgets

from .element import Arrow
from .settings import settings


class Painter(QtGui.QPainter):
  """QPainter customization"""

  def __init__(self, parent=None):
    """Initialisation"""
    super().__init__()
    self.parent = parent

  def drawVline(self, x):
    """Draw a vertical line at x"""
    self.drawLine(
      QtCore.QLineF(
        x * self.parent.width(), 0, x * self.parent.width(), self.parent.height()
      )
    )

  def drawHline(self, y):
    """Draw an horizontal line at y"""
    self.drawLine(
      QtCore.QLineF(
        0, y * self.parent.height(), self.parent.width(), y * self.parent.height()
      )
    )


class PainterScrollArea(QtWidgets.QScrollArea):
  """Painter scrolling Area: QScrollArea around the painterArea."""

  def __init__(self, parent, painterArea):
    """Initialisation"""
    super().__init__(parent)
    self.setAlignment(QtCore.Qt.AlignCenter)
    self.setWidgetResizable(True)
    self.setWidget(painterArea)
    self.painterArea = painterArea

  def wheelEvent(self, event):
    """Wheel event: check if the painterArea intercepted it"""
    if not self.painterArea.on_wheelEvent(event):
      super().wheelEvent(event)
      self.painterArea.lastx = event.position().x() - self.painterArea.pos().x()
      self.painterArea.lasty = event.position().y() - self.painterArea.pos().y()
      self.painterArea.refreshCursor()

  def resizeEvent(self, event):
    """resizeEvent: Apply to self then to painterArea"""
    super().resizeEvent(event)
    self.painterArea.resizeEvent(event)


class PainterArea(QtWidgets.QWidget):
  """Painter Area, where everything is drawn"""

  def __init__(self, parent=None):
    """Initialisation"""
    super().__init__(parent)
    self.setFocus()
    self.setMouseTracking(True)
    self.painter = Painter(self)
    # link to bed main window
    self.parent = parent
    # init of mouse
    self.mousepressed = False
    self.lastx = -1
    self.lasty = -1
    # init of keyboard modifiers
    self.controlpressed = False
    # init of temporary group
    # (group that is create when moving/resizing... a multi-selection)
    self.tmpgroup = False
    # init of resize object flag
    self.resizeObj = None
    # init of mouse wheel flag
    self.wheelObj = None
    # init of rectangular selection flag
    self.rectSelectionOn = False
    # Init of painting area last refresh time
    self.last_refresh = time.time()
    # Init of zooming status
    self.zooming = False
    # Init of scrollArea
    self.scrollArea = PainterScrollArea(parent, self)

  def setSize(self):
    """Compute where to draw the frame given the window size and the frame w/h ratio."""
    sAsize = self.scrollArea.maximumViewportSize()
    w = min(sAsize.width(), round(sAsize.height() * self.parent.document.paper_ratio))
    h = round(w / self.parent.document.paper_ratio)
    if (not self.zooming) or (self.width() <= w and self.height() <= h):
      self.zooming = False
      self.setFixedSize(w, h)

  def resizeEvent(self, event):
    """Recompute the geometry if window is resized"""
    if self.parent.frame is not None:
      self.setSize()

  def paintEvent(self, event):
    """Drawing frame..."""
    self.painter.begin(self)
    if self.parent.isCompiling:
      font = self.painter.font()
      font.setPointSize(20)
      self.painter.setFont(font)
      rect = QtCore.QRect(0, 0, self.width(), self.height())
      self.painter.drawText(
        rect, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter, self.tr('Compiling...')
      )
    elif self.parent.frame is not None:
      # Ask the frame to draw itself at correct position
      self.parent.document.frames[self.parent.frame].draw(
        self.parent.framePage, self.painter
      )
      # Draw the mouse rectangular selection
      if self.rectSelectionOn:
        self.painter.setPen(settings.pen_mouse_selection)
        self.painter.drawRect(self.rectSelectionRect)
    self.painter.end()

  def mousePressEvent(self, event):
    """What to do when mouse is pressed"""
    if (
      QtWidgets.QApplication.overrideCursor()
      and QtWidgets.QApplication.overrideCursor().shape() == QtCore.Qt.OpenHandCursor
    ):
      QtWidgets.QApplication.restoreOverrideCursor()
      QtWidgets.QApplication.setOverrideCursor(
        QtGui.QCursor(QtCore.Qt.ClosedHandCursor)
      )
    if self.parent.frame is not None:
      self.mousepressed = True
      # Reset mouse-moved test
      self.mousemoved = False
      # Unselect wheel object (see wheelEvent)
      self.wheelObj = None
      # Save initial position...
      self.mousepressx = event.position().x()
      self.mousepressy = event.position().y()
      self.lastx = event.position().x()
      self.lasty = event.position().y()
      # If control is not pressed, all previously selected elements are unselected
      if not (
        QtWidgets.QApplication.queryKeyboardModifiers() & QtCore.Qt.ControlModifier
      ):
        # If control is not pressed, unselect all elements
        self.controlpressed = False
        for obj in (
          self.parent.document.frames[self.parent.frame].elements
          + self.parent.document.frames[self.parent.frame].groups
        ):
          obj.selected = False
        self.repaint()
      else:
        self.controlpressed = True

      # Look if an element is under the mouse
      # Reverse the list to prefere to select foreground elements
      for el in reversed(self.parent.document.frames[self.parent.frame].elements):
        obj = el.group if el.group else el
        if obj.hover > 0:
          # The element is under the mouse
          # Toggle selection
          obj.selected = not obj.selected
          self.repaint()
          # Stop to search if something is selected
          return

  def mouseDoubleClickEvent(self, event):
    # Double click -> edit the selected object (or the frame if no selection)
    self.parent.editAny()

  def mouseMoveEvent(self, event):
    """What to do if mouse is moved"""
    if self.parent.frame is not None:
      # If the mouse is pressed
      # There is 2 possibilities
      # 1) we are resizing/moving something
      # 2) we are drawing a rectangular mouse selection
      if self.mousepressed:
        # First time mouse is moved
        if not self.mousemoved:
          if self.controlpressed:
            # Control pressed:
            # There can be 0,1 or more selected elements + the one under mouse:
            hover = 0
            # Look if something under mouse
            for el in reversed(self.parent.document.frames[self.parent.frame].elements):
              obj = el.group if el.group else el
              if obj.hover > 0:
                # Make sure to select the element is under the mouse
                obj.selected = True
                hover = obj.hover if obj.hover < 1100 else 1000
                break
            # If something is found: initialise moving/resizing of the group of selected
            # elements
            if hover > 0:
              # Undo snapshot before doing things
              self.parent.undoStack.doTemp()
              # Save frame groups list
              # Create group
              self.parent.document.frames[self.parent.frame].tmpgroup(
                self.parent.document.paper_ratio
              )
              # Use it as resizing object
              self.resizeObj = self.parent.document.frames[self.parent.frame].groups[-1]
              # If only 1 element in group use the element instead
              if len(self.resizeObj.elements) == 1:
                self.resizeObj = self.resizeObj.elements[0]
                self.resizeObj.refreshHover(
                  self.mousepressx / self.width(), self.mousepressy / self.height()
                )
                self.parent.document.frames[self.parent.frame].untmpgroup()
              else:
                # Remember to delete the group when mouse released
                self.tmpgroup = True
                self.resizeObj.hover = hover
              self.resizeObj.saveGeometry()
          else:
            # Control not pressed: 0 or 1 selected element
            for el in reversed(self.parent.document.frames[self.parent.frame].elements):
              obj = el.group if el.group else el
              if obj.selected:
                # The element is selected
                # Initialise resizing/moving of element
                self.parent.undoStack.doTemp()
                self.resizeObj = obj
                obj.saveGeometry()
        # Remember that mouse already moved
        self.mousemoved = True
        # To avoid to waste computing time
        # Do not refresh to much
        tm = time.time()
        if tm - self.last_refresh > settings.refresh_interval:
          self.last_refresh = tm
          if self.resizeObj:
            # Case 1)
            Dx = (event.position().x() - self.mousepressx) / self.width()
            Dy = (event.position().y() - self.mousepressy) / self.height()
            dx = (event.position().x() - self.lastx) / self.width()
            dy = (event.position().y() - self.lasty) / self.height()
            self.lastx = event.position().x()
            self.lasty = event.position().y()
            # ask the object to resize itself
            self.resizeObj.change_geom(
              Dx,
              Dy,
              dx,
              dy,
              self.parent.document.frames[self.parent.frame].xGuides(
                self.parent.framePage
              ),
              self.parent.document.frames[self.parent.frame].yGuides(
                self.parent.framePage
              ),
            )
          else:
            # Case 2)
            # Draw mouse selection
            self.rectSelectionOn = True
            self.rectSelection(event.position().x(), event.position().y())
          self.repaint()
      else:
        # The mouse is not pressed
        # We look if something is under the mouse to change the shape of the cursor
        # (resizing, moving cursors...)
        self.lastx = event.position().x()
        self.lasty = event.position().y()
        self.refreshCursor()

  def on_wheelEvent(self, event):
    """Wheel event : call wheel function of obj if one is selected"""
    if self.parent.frame is not None:
      if QtWidgets.QApplication.queryKeyboardModifiers() & QtCore.Qt.ControlModifier:
        self.zooming = True
        w = round(self.width() * 1.1 ** (event.angleDelta().y() / 120))
        h = round(w / self.parent.document.paper_ratio)
        x = round(
          event.position().x()
          + (self.pos().x() - event.position().x()) * w / self.width()
        )
        y = round(
          event.position().y()
          + (self.pos().y() - event.position().y()) * h / self.height()
        )
        self.setFixedSize(w, h)
        self.scrollArea.horizontalScrollBar().setValue(-x)
        self.scrollArea.verticalScrollBar().setValue(-y)
        self.lastx = event.position().x() - self.pos().x()
        self.lasty = event.position().y() - self.pos().y()
        self.refreshCursor()
        return True
      for el in reversed(self.parent.document.frames[self.parent.frame].elements):
        # Only arrows have a wheel function (for now)
        if el.selected and type(el) is Arrow and el.hover == 1000:
          # Check if object has changed
          if el != self.wheelObj:
            # Save state before wheel event
            self.parent.undoStack.do()
            # Save which object is selected
            self.wheelObj = el
            el.saveGeometry()
          # object wheel event
          el.wheel(event.angleDelta().x(), event.angleDelta().y())
          self.repaint()
          return True
    return False

  def mouseReleaseEvent(self, event):
    """What to do when mouse is released"""
    # Refresh cursor
    self.refreshCursor()
    if self.parent.frame is not None:
      # If a resizing was initiate but the mouse did not move
      # cancel the undo stack temp (see undo.py)
      if self.resizeObj:
        if self.mousemoved:
          self.parent.undoStack.confirmTemp()
        else:
          self.parent.undoStack.cancelTemp()
      # Re-init variables
      self.mousepressed = False
      self.rectSelectionOn = False
      self.resizeObj = None
      if self.tmpgroup:
        self.parent.document.frames[self.parent.frame].untmpgroup()
        self.tmpgroup = False
      self.repaint()

  def keyPressEvent(self, event):
    """What to do when a key is pressed"""
    if not self.mousepressed:
      self.refreshCursor()  # In case modifiers keys have changed

  def keyReleaseEvent(self, event):
    """What to do when a key is pressed"""
    if not self.mousepressed:
      self.refreshCursor()  # In case modifiers keys have changed

  def refreshCursor(self):
    """Check what is under the mouse to change the shape of the cursor
    (resizing, moving, rotating...)
    """
    if self.parent.frame is not None:
      x = self.lastx / self.width()
      y = self.lasty / self.height()
      hover = 0
      cursor = None
      # Reverse the list to prefere foreground elements
      for el in reversed(self.parent.document.frames[self.parent.frame].elements):
        obj = el.group if el.group else el
        if obj.isvisible(self.parent.framePage):
          hover = obj.refreshHover(x, y)
          if hover > 0:
            # Set cursor shape accordingly
            cursor = obj.selectCursor()
            # Update cursor only if needed
            if not QtWidgets.QApplication.overrideCursor():
              QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(cursor))
            elif QtWidgets.QApplication.overrideCursor().shape() != cursor:
              QtWidgets.QApplication.restoreOverrideCursor()
              QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(cursor))
            # Stop searching if something is found
            break
      # Restore cursor if needed
      if cursor is None and QtWidgets.QApplication.overrideCursor():
        QtWidgets.QApplication.restoreOverrideCursor()

  def rectSelection(self, x, y):
    """Function that decide which elements/groups to select
    when doing a rectangular mouse selection
    """
    # The criterium is that more than half of the element surface
    # must be inside the mouse rectangle
    # Mouse rectangle
    # In painterArea coordinates
    left = min(x, self.mousepressx)
    right = max(x, self.mousepressx)
    top = min(y, self.mousepressy)
    bottom = max(y, self.mousepressy)
    self.rectSelectionRect = QtCore.QRect(left, top, right - left, bottom - top)

    # In frame coordinates
    left = left / self.width()
    right = right / self.width()
    top = top / self.height()
    bottom = bottom / self.height()

    # Find selected objects
    for obj in (
      self.parent.document.frames[self.parent.frame].elements
      + self.parent.document.frames[self.parent.frame].groups
    ):
      if obj.group is None:
        # Object rectangle
        oL = obj.get_xguide('left')
        oR = max(obj.get_xguide('right'), oL + settings.epsilon)  # in case width=0
        oT = obj.get_yguide('top')
        oB = max(obj.get_yguide('bottom'), oT + settings.epsilon)  # in case height=0
        oS = (oR - oL) * (oB - oT)
        # Intersection rectangle
        cL = max(left, oL)
        cR = min(right, oR)
        cT = max(top, oT)
        cB = min(bottom, oB)
        # Intersection surface
        cS = max(0, cR - cL) * max(0, cB - cT)
        # Criterium
        obj.selected = cS > oS / 2 and obj.isvisible(self.parent.framePage)

  def selectAll(self):
    """Select all elements and groups"""
    if self.parent.frame is not None:
      for obj in (
        self.parent.document.frames[self.parent.frame].elements
        + self.parent.document.frames[self.parent.frame].groups
      ):
        # Do not select elements that are contained in a group (just select the group)
        if obj.group is None and obj.isvisible(self.parent.framePage):
          obj.selected = True
      self.repaint()

  def unselectAll(self):
    """Unselect all elements and groups"""
    if self.parent.frame is not None:
      for obj in (
        self.parent.document.frames[self.parent.frame].elements
        + self.parent.document.frames[self.parent.frame].groups
      ):
        if obj.group is None:
          obj.selected = False
      self.repaint()

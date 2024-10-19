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

# This file defines the UndoStack class, that allow to perform undo/redo actions

from .settings import settings


class State:
  """State class defines a complete document state to be saved in the undo/redo stack"""

  def __init__(self, document=None, frame=0, page=0, framePage=0, modified=False):
    """Initialisation"""
    # Deep copy
    self.document = document.copy()
    self.frame = frame
    self.page = page
    self.framePage = framePage
    self.modified = modified

  def copy(self):
    """Deep copy"""
    return State(self.document, self.frame, self.page, self.framePage, self.modified)


class UndoStack:
  """UndoStack class defines an undo/redo stack to save
  and reload intermediate states of the document
  """

  def __init__(self, parent):
    """Initialisation"""
    self.before_states = []
    self.after_states = []
    self.parent = parent
    self.tempState = None
    self.parent.modified = False

  def getState(self):
    """Get the current state of the document from parent"""
    return State(
      self.parent.document,
      self.parent.frame,
      self.parent.page,
      self.parent.framePage,
      self.parent.modified,
    )

  def setState(self, state):
    """Set the current state of the document to "state" """
    self.parent.document = state.document
    self.parent.frame = state.frame
    self.parent.page = state.page
    self.parent.framePage = state.framePage
    self.parent.modified = state.modified
    self.parent.makeFrameList()
    self.parent.makePageList()
    self.parent.makeFramePageList()
    self.parent.setIndexes()
    self.parent.painterArea.repaint()

  def do(self, current_state=None):
    """Save the current state in the stack before doing a modifications"""
    # Here is the behavior:
    # If the user do actions A, then B then C
    # Then undo action C and B (go back to A state)
    # Then modify the document (action D)
    # The undo stack will be A,B,C,B,A,D
    if not current_state:
      current_state = self.getState()
    self.before_states.append(current_state)
    # If there are some redo actions in after_states
    # We are in the case described at the beginning of the function
    # So we copy states in the after_states list twice (ABCBA..)
    if self.after_states != []:
      for state in reversed(self.after_states[1:]):
        self.before_states.append(state.copy())
      self.before_states += self.after_states
      self.before_states.append(current_state.copy())
      self.after_states = []
    # Remove old preview images from memory (to avoid memory leakage)
    for state in self.before_states[: -settings.Nkeep_previews]:
      state.document.clean_imgs()
    self.parent.modified = True

  def doTemp(self):
    """Do a temporary state save.
    This state can be confirmed later and put in the stack,
    can be reloaded in the document, or completely forgotten and deleted.
    """
    self.tempState = self.getState()

  def confirmTemp(self):
    """Confirm the last temp state"""
    if self.tempState:
      self.do(self.tempState)
      self.tempState = None

  def cancelTemp(self):
    """Cancel (forget) the last temp state"""
    self.tempState = None

  def reloadTemp(self):
    """Reload the last temp state"""
    if self.tempState:
      self.setState(self.tempState)
      self.tempState = None

  def undo(self):
    """Undo function, load the previous state in the undo stack"""
    if self.before_states != []:
      self.after_states.append(self.getState())
      self.setState(self.before_states.pop())

  def redo(self):
    """Redo function, load the next state undo stack"""
    if self.after_states != []:
      self.before_states.append(self.getState())
      self.setState(self.after_states.pop())

  def updateModified(self):
    """Update all states modified field if the document has been saved"""
    self.parent.modified = False
    for state in self.before_states + self.after_states:
      state.modified = True

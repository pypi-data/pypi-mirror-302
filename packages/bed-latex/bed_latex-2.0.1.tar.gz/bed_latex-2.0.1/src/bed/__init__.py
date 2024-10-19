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

# This the main file of BEd
# It creates the main window
# and all the user-callable functions (using the menu, shortcuts...)

# Important vocabulary conventions:
# When compiling a Beamer presentation in pdf,
# a single Beamer "frame" can be spread over several pdf "pages",
# if the frame contains some overlay commands (\only...).
# "frame" corresponds to the Beamer definition
# "page" refers to the pages in the final pdf
# "framePage" corresponds to the page number in a given Beamer frame

import html
import os
import re
import sys
import tempfile
import traceback

from PySide6 import QtCore, QtGui, QtWidgets

from . import parsing
from .document import Document
from .element import Arrow, Image, Text, TikzPicture
from .frame import Frame
from .group import Group
from .helpers import striplines
from .painter import PainterArea
from .settings import settings
from .undo import UndoStack

_exec_path = os.path.dirname(os.path.realpath(__file__))
_icons_path = f'{_exec_path}/icons'
_tr_path = f'{_exec_path}/translation'
_latex_path = f'{_exec_path}/latex'


class BEd(QtWidgets.QMainWindow):
  def __init__(self):
    """Initialisation of application"""
    super().__init__()
    self.compileOutput = tempfile.NamedTemporaryFile(prefix='bed-', suffix='.log').name
    self.document = None
    self.tmpFile = None
    self.frame = None
    self.framePage = None
    self.isCompiling = False
    self.copyList = []
    # Init of the window properties...
    self.setMinimumSize(550, 550)
    # set initial size of window (from config file)
    self.resize(settings.window_width, settings.window_height)
    self.setWindowTitle('BEd')
    self.setWindowIcon(QtGui.QIcon(f'{_icons_path}/bed.svg'))
    # Init of the area where presentation slides will be drawn (painterArea)
    self.painterArea = PainterArea(self)
    self.setCentralWidget(self.painterArea.scrollArea)
    self.painterArea.setFocus()
    # Init of actions, menus, pagebar
    self.initMenus()
    self.show()

  def initDocument(self, filename=None, page=0):
    """Initialisation of document"""
    if filename is not None:
      # If filename is passed in arg open the file
      self.openFile(filename, page)
      # Init of undo/redo stack
      self.undoStack = UndoStack(self)
    else:
      # Else start a new document from scratch
      self.newDoc()
      # Go to home directory
      os.chdir(os.path.expanduser('~'))

  def initMenus(self):
    """Initialisation of menus..."""
    # Status bar
    self.statusBar()

    # Cleaning previously defined actions
    # Needed to avoid shortcuts ambiguity when doing a resetUI
    for action in self.actions():
      self.removeAction(action)

    # Actions and shortcuts (from config file)
    newDocAction = QtGui.QAction(
      QtGui.QIcon.fromTheme(
        'document-new', QtGui.QIcon(f'{_icons_path}/document-new.svg')
      ),
      self.tr('&New document'),
      self,
    )
    newDocAction.setShortcut(QtGui.QKeySequence.New)
    newDocAction.setStatusTip(self.tr('Start a new document', 'BEd'))
    newDocAction.triggered.connect(self.newDoc)
    self.addAction(newDocAction)

    openAction = QtGui.QAction(
      QtGui.QIcon.fromTheme(
        'document-open', QtGui.QIcon(f'{_icons_path}/document-open.svg')
      ),
      self.tr('&Open'),
      self,
    )
    openAction.setShortcut(QtGui.QKeySequence.Open)
    openAction.setStatusTip(self.tr('Open TeX file'))
    openAction.triggered.connect(self.openDialog)
    self.addAction(openAction)

    reloadAction = QtGui.QAction(
      QtGui.QIcon.fromTheme(
        'view-refresh', QtGui.QIcon(f'{_icons_path}/view-refresh.svg')
      ),
      self.tr('&Reload'),
      self,
    )
    reloadAction.setShortcut(QtGui.QKeySequence(settings.shortcut_reload))
    reloadAction.setStatusTip(self.tr('Reload TeX file'))
    reloadAction.triggered.connect(self.reloadTeX)
    self.addAction(reloadAction)

    previewAction = QtGui.QAction(
      QtGui.QIcon.fromTheme(
        'view-preview', QtGui.QIcon(f'{_icons_path}/view-preview.svg')
      ),
      self.tr('&Preview'),
      self,
    )
    previewAction.setShortcut(QtGui.QKeySequence(settings.shortcut_preview))
    previewAction.setStatusTip(self.tr('Preview current frame'))
    previewAction.triggered.connect(self.previewCurrentFrame)
    self.addAction(previewAction)

    saveAction = QtGui.QAction(
      QtGui.QIcon.fromTheme(
        'document-save', QtGui.QIcon(f'{_icons_path}/document-save.svg')
      ),
      self.tr('&Save'),
      self,
    )
    saveAction.setShortcut(QtGui.QKeySequence.Save)
    if settings.auto_reload:
      saveAction.setStatusTip(self.tr('Save TeX file, compile, and reload'))
    else:
      saveAction.setStatusTip(self.tr('Save TeX file'))
    saveAction.triggered.connect(self.save)
    self.addAction(saveAction)

    saveAsAction = QtGui.QAction(
      QtGui.QIcon.fromTheme(
        'document-save-as', QtGui.QIcon(f'{_icons_path}/document-save-as.svg')
      ),
      self.tr('Save &as...'),
      self,
    )
    saveAsAction.setShortcut(QtGui.QKeySequence.SaveAs)
    if settings.auto_reload:
      saveAsAction.setStatusTip(self.tr('Save TeX file as..., compile, and reload'))
    else:
      saveAsAction.setStatusTip(self.tr('Save TeX file as...'))
    saveAsAction.triggered.connect(self.saveAs)
    self.addAction(saveAsAction)

    exitAction = QtGui.QAction(
      QtGui.QIcon.fromTheme(
        'application-exit', QtGui.QIcon(f'{_icons_path}/application-exit.svg')
      ),
      self.tr('&Exit'),
      self,
    )
    exitAction.setShortcut(QtGui.QKeySequence.Quit)
    exitAction.setStatusTip(self.tr('Exit application'))
    exitAction.triggered.connect(self.close)
    self.addAction(exitAction)

    previousPageAction = QtGui.QAction(
      QtGui.QIcon.fromTheme(
        'go-previous', QtGui.QIcon(f'{_icons_path}/go-previous.svg')
      ),
      self.tr('Previous page'),
      self,
    )
    previousPageAction.setShortcut(QtGui.QKeySequence.MoveToPreviousChar)
    previousPageAction.setStatusTip(self.tr('Go to the previous page'))
    previousPageAction.triggered.connect(self.previousPage)
    self.addAction(previousPageAction)

    nextPageAction = QtGui.QAction(
      QtGui.QIcon.fromTheme('go-next', QtGui.QIcon(f'{_icons_path}/go-next.svg')),
      self.tr('Next page'),
      self,
    )
    nextPageAction.setShortcut(QtGui.QKeySequence.MoveToNextChar)
    nextPageAction.setStatusTip(self.tr('Go to the next page'))
    nextPageAction.triggered.connect(self.nextPage)
    self.addAction(nextPageAction)

    selectAllAction = QtGui.QAction(
      QtGui.QIcon.fromTheme(
        'edit-select-all', QtGui.QIcon(f'{_icons_path}/edit-select-all.svg')
      ),
      self.tr('Select &all...'),
      self,
    )
    selectAllAction.setShortcut(QtGui.QKeySequence.SelectAll)
    selectAllAction.setStatusTip(self.tr('Select all objects in current frame'))
    selectAllAction.triggered.connect(self.painterArea.selectAll)
    self.addAction(selectAllAction)

    unselectAllAction = QtGui.QAction(
      QtGui.QIcon.fromTheme(
        'dialog-cancel', QtGui.QIcon(f'{_icons_path}/dialog-cancel.svg')
      ),
      self.tr('Unselect &all...'),
      self,
    )
    unselectAllAction.setShortcut(QtGui.QKeySequence.Deselect)
    unselectAllAction.setStatusTip(self.tr('Unselect all objects in current frame'))
    unselectAllAction.triggered.connect(self.painterArea.unselectAll)
    self.addAction(unselectAllAction)

    editAction = QtGui.QAction(
      QtGui.QIcon.fromTheme(
        'document-edit', QtGui.QIcon(f'{_icons_path}/document-edit.svg')
      ),
      self.tr('&Edit...'),
      self,
    )
    editAction.setShortcut(QtGui.QKeySequence(settings.shortcut_edit))
    editAction.setStatusTip(self.tr('Edit selected objects'))
    editAction.triggered.connect(self.editAnyConnect)
    self.addAction(editAction)

    editDocAction = QtGui.QAction(
      QtGui.QIcon.fromTheme(
        'story-editor', QtGui.QIcon(f'{_icons_path}/story-editor.svg')
      ),
      self.tr('Edit &document'),
      self,
    )
    editDocAction.setShortcut(QtGui.QKeySequence(settings.shortcut_editDoc))
    editDocAction.setStatusTip(self.tr('Edit document parameters (LaTeX header...)'))
    editDocAction.triggered.connect(self.editDoc)
    self.addAction(editDocAction)

    copyAction = QtGui.QAction(
      QtGui.QIcon.fromTheme('edit-copy', QtGui.QIcon(f'{_icons_path}/edit-copy.svg')),
      self.tr('&Copy'),
      self,
    )
    copyAction.setShortcut(QtGui.QKeySequence.Copy)
    copyAction.setStatusTip(self.tr('Copy selected objects'))
    copyAction.triggered.connect(self.copyAny)
    self.addAction(copyAction)

    cutAction = QtGui.QAction(
      QtGui.QIcon.fromTheme('edit-cut', QtGui.QIcon(f'{_icons_path}/edit-cut.svg')),
      self.tr('&Cut'),
      self,
    )
    cutAction.setShortcut(QtGui.QKeySequence.Cut)
    cutAction.setStatusTip(self.tr('Cut selected objects'))
    cutAction.triggered.connect(self.cutAny)
    self.addAction(cutAction)

    pasteAction = QtGui.QAction(
      QtGui.QIcon.fromTheme('edit-paste', QtGui.QIcon(f'{_icons_path}/edit-paste.svg')),
      self.tr('&Paste'),
      self,
    )
    pasteAction.setShortcut(QtGui.QKeySequence.Paste)
    pasteAction.setStatusTip(self.tr('Paste selected objects'))
    pasteAction.triggered.connect(self.pasteAny)
    self.addAction(pasteAction)

    deleteAction = QtGui.QAction(
      QtGui.QIcon.fromTheme(
        'edit-delete', QtGui.QIcon(f'{_icons_path}/edit-delete.svg')
      ),
      self.tr('&Delete'),
      self,
    )
    deleteAction.setShortcut(QtGui.QKeySequence.Delete)
    deleteAction.setStatusTip(self.tr('Delete selected objects'))
    deleteAction.triggered.connect(self.deleteAny)
    self.addAction(deleteAction)

    undoAction = QtGui.QAction(
      QtGui.QIcon.fromTheme('edit-undo', QtGui.QIcon(f'{_icons_path}/edit-undo.svg')),
      self.tr('&Undo'),
      self,
    )
    undoAction.setShortcut(QtGui.QKeySequence.Undo)
    undoAction.setStatusTip(self.tr('Undo last action'))
    undoAction.triggered.connect(self.undo)
    self.addAction(undoAction)

    redoAction = QtGui.QAction(
      QtGui.QIcon.fromTheme('edit-redo', QtGui.QIcon(f'{_icons_path}/edit-redo.svg')),
      self.tr('&Redo'),
      self,
    )
    redoAction.setShortcut(QtGui.QKeySequence.Redo)
    redoAction.setStatusTip(self.tr('Redo action'))
    redoAction.triggered.connect(self.redo)
    self.addAction(redoAction)

    groupAction = QtGui.QAction(
      QtGui.QIcon.fromTheme(
        'object-group', QtGui.QIcon(f'{_icons_path}/object-group.svg')
      ),
      self.tr('&Group'),
      self,
    )
    groupAction.setShortcut(QtGui.QKeySequence(settings.shortcut_group))
    groupAction.setStatusTip(self.tr('Group selected objects'))
    groupAction.triggered.connect(self.group)
    self.addAction(groupAction)

    ungroupAction = QtGui.QAction(
      QtGui.QIcon.fromTheme(
        'object-ungroup', QtGui.QIcon(f'{_icons_path}/object-ungroup.svg')
      ),
      self.tr('&Ungroup'),
      self,
    )
    ungroupAction.setShortcut(QtGui.QKeySequence(settings.shortcut_ungroup))
    ungroupAction.setStatusTip(self.tr('Ungroup selected objects'))
    ungroupAction.triggered.connect(self.ungroup)
    self.addAction(ungroupAction)

    newFrameAction = QtGui.QAction(
      QtGui.QIcon.fromTheme('window-new', QtGui.QIcon(f'{_icons_path}/window-new.svg')),
      self.tr('New &frame'),
      self,
    )
    newFrameAction.setShortcut(QtGui.QKeySequence(settings.shortcut_newFrame))
    newFrameAction.setStatusTip(self.tr('Add a new frame'))
    newFrameAction.triggered.connect(self.newFrame)
    self.addAction(newFrameAction)

    newFrameTemplateActions = []
    for ktemp in range(len(settings.templates) // 2):
      newFrameTemplateActions.append(
        QtGui.QAction(
          QtGui.QIcon.fromTheme(
            'project-development-new-template',
            QtGui.QIcon(f'{_icons_path}/project-development-new-template.svg'),
          ),
          self.tr('Template') + f' &{ktemp + 1} "{settings.templates[2 * ktemp]}"',
          self,
        )
      )
      newFrameTemplateActions[-1].setShortcut(
        QtGui.QKeySequence(settings.shortcut_newFrameTemplate + f'+{ktemp + 1}')
      )
      newFrameTemplateActions[-1].setStatusTip(
        self.tr('Add a new frame from the template')
        + f' "{settings.templates[2 * ktemp]}"'
      )
      newFrameTemplateActions[-1].triggered.connect(
        lambda _, who=ktemp: self.newFrameTemplate(who)
      )
      self.addAction(newFrameTemplateActions[-1])

    saveTemplateAction = QtGui.QAction(
      QtGui.QIcon.fromTheme(
        'document-save-as-template',
        QtGui.QIcon(f'{_icons_path}/document-save-as-template.svg'),
      ),
      self.tr('Save &template'),
      self,
    )
    saveTemplateAction.setShortcut(QtGui.QKeySequence(settings.shortcut_saveTemplate))
    saveTemplateAction.setStatusTip(self.tr('Save current frame as template'))
    saveTemplateAction.triggered.connect(self.saveTemplate)
    self.addAction(saveTemplateAction)

    deleteTemplateAction = QtGui.QAction(
      QtGui.QIcon(f'{_icons_path}/project-development-delete-template.svg'),
      self.tr('&Delete template'),
      self,
    )
    deleteTemplateAction.setShortcut(
      QtGui.QKeySequence(settings.shortcut_deleteTemplate)
    )
    deleteTemplateAction.setStatusTip(self.tr('Delete one of the saved templates'))
    deleteTemplateAction.triggered.connect(self.deleteTemplate)
    self.addAction(deleteTemplateAction)

    newTextAction = QtGui.QAction(
      QtGui.QIcon.fromTheme(
        'insert-text-frame', QtGui.QIcon(f'{_icons_path}/insert-text-frame.svg')
      ),
      self.tr('New &text'),
      self,
    )
    newTextAction.setShortcut(QtGui.QKeySequence(settings.shortcut_newText))
    newTextAction.setStatusTip(self.tr('Add a new text block'))
    newTextAction.triggered.connect(self.newText)
    self.addAction(newTextAction)

    newImageAction = QtGui.QAction(
      QtGui.QIcon.fromTheme(
        'insert-image', QtGui.QIcon(f'{_icons_path}/insert-image.svg')
      ),
      self.tr('New &image'),
      self,
    )
    newImageAction.setShortcut(QtGui.QKeySequence(settings.shortcut_newImage))
    newImageAction.setStatusTip(self.tr('Add a new image'))
    newImageAction.triggered.connect(self.newImage)
    self.addAction(newImageAction)

    newTikzPictureAction = QtGui.QAction(
      QtGui.QIcon.fromTheme(
        'draw-triangle', QtGui.QIcon(f'{_icons_path}/draw-triangle.svg')
      ),
      self.tr('New &Tikz picture'),
      self,
    )
    newTikzPictureAction.setShortcut(
      QtGui.QKeySequence(settings.shortcut_newTikzPicture)
    )
    newTikzPictureAction.setStatusTip(self.tr('Add a new Tikz picture'))
    newTikzPictureAction.triggered.connect(self.newTikzPicture)
    self.addAction(newTikzPictureAction)

    newArrowAction = QtGui.QAction(
      QtGui.QIcon.fromTheme('draw-line', QtGui.QIcon(f'{_icons_path}/draw-line.svg')),
      self.tr('New &arrow'),
      self,
    )
    newArrowAction.setShortcut(QtGui.QKeySequence(settings.shortcut_newArrow))
    newArrowAction.setStatusTip(self.tr('Add a new arrow'))
    newArrowAction.triggered.connect(self.newArrow)
    self.addAction(newArrowAction)

    moveUpAction = QtGui.QAction(
      QtGui.QIcon.fromTheme('go-up', QtGui.QIcon(f'{_icons_path}/go-up.svg')),
      self.tr('Move &up'),
      self,
    )
    moveUpAction.setShortcut(QtGui.QKeySequence(settings.shortcut_moveUp))
    moveUpAction.setStatusTip(self.tr('Move up selection a notch'))
    moveUpAction.triggered.connect(self.moveUp)
    self.addAction(moveUpAction)

    moveDownAction = QtGui.QAction(
      QtGui.QIcon.fromTheme('go-down', QtGui.QIcon(f'{_icons_path}/go-down.svg')),
      self.tr('Move &down'),
      self,
    )
    moveDownAction.setShortcut(QtGui.QKeySequence(settings.shortcut_moveDown))
    moveDownAction.setStatusTip(self.tr('Move down selection a notch'))
    moveDownAction.triggered.connect(self.moveDown)
    self.addAction(moveDownAction)

    moveTopAction = QtGui.QAction(
      QtGui.QIcon.fromTheme('go-top', QtGui.QIcon(f'{_icons_path}/go-top.svg')),
      self.tr('Move &top'),
      self,
    )
    moveTopAction.setShortcut(QtGui.QKeySequence(settings.shortcut_moveTop))
    moveTopAction.setStatusTip(self.tr('Move selection to top level'))
    moveTopAction.triggered.connect(self.moveTop)
    self.addAction(moveTopAction)

    moveBottomAction = QtGui.QAction(
      QtGui.QIcon.fromTheme('go-bottom', QtGui.QIcon(f'{_icons_path}/go-bottom.svg')),
      self.tr('Move &bottom'),
      self,
    )
    moveBottomAction.setShortcut(QtGui.QKeySequence(settings.shortcut_moveBottom))
    moveBottomAction.setStatusTip(self.tr('Move selection to bottom level'))
    moveBottomAction.triggered.connect(self.moveBottom)
    self.addAction(moveBottomAction)

    self.activateGridAction = QtGui.QAction(
      QtGui.QIcon.fromTheme(
        'grid-rectangular', QtGui.QIcon(f'{_icons_path}/grid-rectangular.svg')
      ),
      self.tr('&Grid'),
      self,
      checkable=True,
    )
    self.activateGridAction.setShortcut(
      QtGui.QKeySequence(settings.shortcut_activateGrid)
    )
    self.activateGridAction.setStatusTip(self.tr('(De)activate grid guides'))
    self.activateGridAction.setChecked(settings.activate_grid)
    self.activateGridAction.triggered.connect(self.toggleGrid)
    self.addAction(self.activateGridAction)

    self.activateObjGuidesAction = QtGui.QAction(
      QtGui.QIcon.fromTheme(
        'format-border-set-all', QtGui.QIcon(f'{_icons_path}/format-border-set-all.svg')
      ),
      self.tr('&Object guides'),
      self,
      checkable=True,
    )
    self.activateObjGuidesAction.setShortcut(
      QtGui.QKeySequence(settings.shortcut_activateObjGuides)
    )
    self.activateObjGuidesAction.setStatusTip(self.tr('(De)activate object guides'))
    self.activateObjGuidesAction.setChecked(settings.activate_object_guides)
    self.activateObjGuidesAction.triggered.connect(self.toggleObjGuides)
    self.addAction(self.activateObjGuidesAction)

    self.showHiddenObjectsAction = QtGui.QAction(
      QtGui.QIcon.fromTheme('visibility', QtGui.QIcon(f'{_icons_path}/visibility.svg')),
      self.tr('&Hidden objects'),
      self,
      checkable=True,
    )
    self.showHiddenObjectsAction.setShortcut(
      QtGui.QKeySequence(settings.shortcut_showHiddenObjects)
    )
    self.showHiddenObjectsAction.setStatusTip(self.tr('Reveal hidden objects'))
    self.showHiddenObjectsAction.setChecked(settings.show_hidden_objects)
    self.showHiddenObjectsAction.triggered.connect(self.toggleHiddenObjects)
    self.addAction(self.showHiddenObjectsAction)

    self.hideMenuAction = QtGui.QAction(
      QtGui.QIcon.fromTheme('show-menu', QtGui.QIcon(f'{_icons_path}/show-menu.svg')),
      self.tr('Show/Hide &menu'),
      self,
      checkable=True,
    )
    self.hideMenuAction.setShortcut(QtGui.QKeySequence(settings.shortcut_hideMenu))
    self.hideMenuAction.setStatusTip(self.tr('Show/Hide menu bar'))
    self.hideMenuAction.setChecked(settings.menuVisible)
    self.hideMenuAction.triggered.connect(self.toggleMenu)
    self.addAction(self.hideMenuAction)

    editSettingsAction = QtGui.QAction(
      QtGui.QIcon.fromTheme(
        'document-edit', QtGui.QIcon(f'{_icons_path}/document-edit.svg')
      ),
      self.tr('&Edit settings'),
      self,
    )
    editSettingsAction.setShortcut(QtGui.QKeySequence(settings.shortcut_editSettings))
    editSettingsAction.setStatusTip(self.tr('Edit settings'))
    editSettingsAction.triggered.connect(self.editSettings)
    self.addAction(editSettingsAction)

    saveSettingsAction = QtGui.QAction(
      QtGui.QIcon.fromTheme(
        'document-save', QtGui.QIcon(f'{_icons_path}/document-save.svg')
      ),
      self.tr('&Save settings'),
      self,
    )
    saveSettingsAction.setShortcut(QtGui.QKeySequence(settings.shortcut_saveSettings))
    saveSettingsAction.setStatusTip(self.tr('Save current settings'))
    saveSettingsAction.triggered.connect(settings.write)
    self.addAction(saveSettingsAction)

    self.autoSaveSettingsAction = QtGui.QAction(
      QtGui.QIcon.fromTheme(
        'document-save', QtGui.QIcon(f'{_icons_path}/document-save.svg')
      ),
      self.tr('&Auto save settings'),
      self,
      checkable=True,
    )
    self.autoSaveSettingsAction.setShortcut(
      QtGui.QKeySequence(settings.shortcut_autoSaveSettings)
    )
    self.autoSaveSettingsAction.setStatusTip(
      self.tr('Automatically save settings on exit')
    )
    self.autoSaveSettingsAction.setChecked(settings.auto_save_settings)
    self.autoSaveSettingsAction.triggered.connect(self.toggleAutoSaveSettings)
    self.addAction(self.autoSaveSettingsAction)

    # Menubar
    self.menu = self.menuBar()
    # Clearing menu before repopulating it (in case of UI re-init)
    self.menu.clear()
    self.menu.setVisible(settings.menuVisible)
    fileMenu = self.menu.addMenu(self.tr('&File'))
    fileMenu.addAction(newDocAction)
    fileMenu.addAction(openAction)
    fileMenu.addAction(reloadAction)
    fileMenu.addAction(previewAction)
    fileMenu.addAction(saveAction)
    fileMenu.addAction(saveAsAction)
    fileMenu.addAction(exitAction)

    editMenu = self.menu.addMenu(self.tr('&Edit'))
    editMenu.addAction(undoAction)
    editMenu.addAction(redoAction)
    editMenu.addAction(selectAllAction)
    editMenu.addAction(unselectAllAction)
    editMenu.addAction(copyAction)
    editMenu.addAction(cutAction)
    editMenu.addAction(pasteAction)
    editMenu.addAction(deleteAction)
    editMenu.addAction(editDocAction)
    editMenu.addAction(editAction)
    editMenu.addAction(groupAction)
    editMenu.addAction(ungroupAction)

    insertMenu = self.menu.addMenu(self.tr('&Insert'))
    insertMenu.addAction(newTextAction)
    insertMenu.addAction(newImageAction)
    insertMenu.addAction(newTikzPictureAction)
    insertMenu.addAction(newArrowAction)
    insertMenu.addAction(newFrameAction)
    for tempAct in newFrameTemplateActions:
      insertMenu.addAction(tempAct)
    insertMenu.addAction(saveTemplateAction)
    insertMenu.addAction(deleteTemplateAction)

    moveMenu = self.menu.addMenu(self.tr('&Depth'))
    moveMenu.addAction(moveUpAction)
    moveMenu.addAction(moveDownAction)
    moveMenu.addAction(moveTopAction)
    moveMenu.addAction(moveBottomAction)

    configMenu = self.menu.addMenu(self.tr('&Configuration'))
    configMenu.addAction(self.activateGridAction)
    configMenu.addAction(self.activateObjGuidesAction)
    configMenu.addAction(self.showHiddenObjectsAction)
    configMenu.addAction(self.hideMenuAction)
    configMenu.addAction(editSettingsAction)
    configMenu.addAction(saveSettingsAction)
    configMenu.addAction(self.autoSaveSettingsAction)

    # Page bar (bottom of main window, combobox for the page, frame and framePage)
    # spacer used to center widgets on pagebar
    pagespaceL = QtWidgets.QWidget()
    pagespaceL.setSizePolicy(
      QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding
    )
    pagespaceR = QtWidgets.QWidget()
    pagespaceR.setSizePolicy(
      QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding
    )
    frameLabel = QtWidgets.QLabel(self)
    frameLabel.setText(self.tr('Frame'))
    pageLabel = QtWidgets.QLabel(self)
    pageLabel.setText(self.tr('Page'))
    framePageLabel = QtWidgets.QLabel(self)
    framePageLabel.setText(self.tr('Page in Frame'))
    self.frameCombo = QtWidgets.QComboBox(self)
    self.frameCombo.currentIndexChanged.connect(self.changeFrame)
    self.pageCombo = QtWidgets.QComboBox(self)
    self.pageCombo.currentIndexChanged.connect(self.changePage)
    self.framePageCombo = QtWidgets.QComboBox(self)
    self.framePageCombo.currentIndexChanged.connect(self.changeFramePage)

    # Remove pagebar before reinserting it (in case of UI re-init)
    if hasattr(self, 'pagebar'):
      self.pagebar.visibilityChanged.disconnect()
      self.removeToolBar(self.pagebar)
    self.pagebar = QtWidgets.QToolBar(self.tr('Pagebar'), self)
    self.addToolBar(QtCore.Qt.BottomToolBarArea, self.pagebar)
    self.pagebar.setVisible(settings.pagebarVisible)
    self.pagebar.visibilityChanged.connect(self.togglePagebar)
    self.pagebar.setFloatable(False)
    self.pagebar.setMovable(False)
    self.pagebar.setStyleSheet('QToolBar{spacing:5px;}')
    self.pagebar.addWidget(pagespaceL)
    self.pagebar.addAction(previousPageAction)
    self.pagebar.addWidget(frameLabel)
    self.pagebar.addWidget(self.frameCombo)
    self.pagebar.addSeparator()
    self.pagebar.addWidget(pageLabel)
    self.pagebar.addWidget(self.pageCombo)
    self.pagebar.addSeparator()
    self.pagebar.addWidget(framePageLabel)
    self.pagebar.addWidget(self.framePageCombo)
    self.pagebar.addAction(nextPageAction)
    self.pagebar.addWidget(pagespaceR)

  def resetUI(self):
    self.initMenus()
    self.makeFrameList()
    self.makePageList()
    self.makeFramePageList()
    self.setIndexes()
    self.painterArea.repaint()

  def resizeEvent(self, event):
    """Things to do when the user resize the window"""
    # Most important resizing consequences are treated by the painterArea resizeEvent
    # Here we just save the new size in the application settings
    settings.window_width = self.width()
    settings.window_height = self.height()

  def newDoc(self):
    """Start a new document from scratch"""
    # If a doc is already opened
    # check if all changes have been saved
    # before starting another one
    if self.document and not self.checkSaved():
      return False
    # Re-init variables
    self.filename = None
    self.folder = None
    self.tmpFile = None
    self.frame = 0
    self.page = 0
    self.framePage = 0
    # Create new doc with a single frame (single page)
    self.document = Document(
      settings.default_header,
      settings.default_footer,
      [Frame(title=settings.default_newdoc_frame_title)],
      settings.default_paper_w,
      settings.default_paper_h,
      1,
    )
    # Re-adjust the size of the painter area
    self.painterArea.setSize()
    # Init of frame, page, framePage combobox
    self.makeFrameList()
    self.makePageList()
    self.makeFramePageList()
    self.setIndexes()
    # Re-Init of undo/redo stack
    self.undoStack = UndoStack(self)
    # Show a preview of the document
    self.previewCurrentFrame()
    return True

  def openDialog(self):
    """Dialog asking for a tex file to open"""
    # Check if all changes have been saved in current doc
    # before opening another one
    if self.checkSaved():
      # Prevent actions in main window (see painter.py) while the dialog is shown
      # Reset mouse cursor to default (remove resize, move... cursors)
      QtWidgets.QApplication.restoreOverrideCursor()
      filename = QtWidgets.QFileDialog.getOpenFileName(
        self, self.tr('Open File'), '.', 'TeX (*.tex)'
      )[0]
      if filename != '':
        # Re-init tmpFile backup
        if self.tmpFile:
          os.remove(self.tmpFile)
          self.tmpFile = None
        # Open the file
        self.openFile(filename)
        # Re-init undo/redo stack
        self.undoStack = UndoStack(self)

  def openFile(self, filename, page=0, reloadAfterSave=False):
    """Open existing tex file given in argument"""
    self.isCompiling = True
    self.painterArea.repaint()
    # Separate folder and filename
    spFolderFile = re.split(r'/', filename)
    folder = r'/'.join(spFolderFile[:-1])
    if folder == '':
      folder = os.getcwd()
    folder += '/'
    # Change working directory to the tex file directory
    os.chdir(folder)
    # Store current folder
    self.folder = folder
    # Separate filename and extension (.tex)
    spNameExt = re.split(r'\.', spFolderFile[-1])
    if spNameExt[-1] == 'tex':
      self.filename = '.'.join(spNameExt[:-1])
    else:
      self.filename = spFolderFile[-1]
    # Compile the tex file
    if not self.compileTeX():
      # If the pdf was not produced (something is broken in the tex file)
      # Ask the user what to do
      self.compileIssueDialog(reloadAfterSave)
      self.isCompiling = False
      self.painterArea.repaint()
      return
    # Re-init document
    self.document = Document()
    # Load document infos (frames, text blocks, images...) from tex and log files
    try:
      self.document.readDoc(self.filename)
    except parsing.MissingBEdLatexPackageError:
      msg = QtWidgets.QMessageBox(self)
      msg.setIcon(QtWidgets.QMessageBox.Warning)
      msg.setWindowTitle(self.tr('LaTeX error detected'))
      msg.setText(
        self.tr(
          'BEd can only load LaTeX files that include the bed LaTeX package. '
          'Please add "\\usepackage{bed}" in the preamble of the file and retry.'
        )
      )
      msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
      msg.exec_()
      self.filename = None
      self.document = None
      self.frame = None
      self.isCompiling = False
      self.painterArea.repaint()
      return
    # Re-adjust the size of the painter area
    self.painterArea.setSize()
    self.page = min(page, self.document.npages - 1)
    # Init of frame, page, framePage combobox
    self.frameFromPage()
    self.makeFrameList()
    self.makePageList()
    self.makeFramePageList()
    self.setIndexes()
    # If tmpFile does not exist create it
    if not self.tmpFile:
      self.tmpFile = tempfile.NamedTemporaryFile(prefix='bed-', suffix='.tex').name
    # Copy current working tex in tmpFile
    os.system('cp "' + self.filename + '.tex" ' + self.tmpFile)
    self.isCompiling = False
    self.painterArea.repaint()

  def compileTeX(self):
    """Compile the current tex file to produce the pdf (system command "pdflatex")
    Check if pdf is produced
    """
    if self.filename:
      # remove old pdf
      if os.path.isfile(self.filename + '.pdf'):
        os.remove(self.filename + '.pdf')
      # compile tex
      os.system(
        settings.latex_cmd
        + ' "'
        + self.filename
        + '.tex" | grep Error > '
        + self.compileOutput
      )
      # Return if the pdf has been produced and no errors have been detected
      return (
        os.path.isfile(self.filename + '.pdf')
        and os.stat(self.compileOutput).st_size == 0
      )
    return False

  def compileIssueDialog(self, reloadAfterSave=False):
    """Ask the user what to do if TeX file compiling did not work"""
    # Reset mouse cursor to default (remove resize, move... cursors)
    QtWidgets.QApplication.restoreOverrideCursor()
    msg = QtWidgets.QMessageBox(self)
    msg.setIcon(QtWidgets.QMessageBox.Warning)
    msg.setWindowTitle(self.tr('LaTeX error detected'))
    with open(self.compileOutput) as cf:
      err = cf.read()
    # Get the previous working tex file if it exists
    if self.tmpFile:
      # Copy backup in working directory
      os.system('cp ' + self.tmpFile + ' "' + self.filename + '.tex.bak"')
      msg.setText(
        self.tr(
          'The document could not be compiled. '
          'The previous saved version of the document has been copied '
          'in the current directory with a .bak extension. '
          'Do you want to reset the document to this backup '
          '(you will lose all changes made) '
          'or continue to edit the current non-working version to try and fix it?'
        )
        + f'\n\n{err}'
      )
      msg.setStandardButtons(QtWidgets.QMessageBox.Reset | QtWidgets.QMessageBox.Retry)
      answer = msg.exec_()
      if answer == QtWidgets.QMessageBox.Reset:
        # If user ask for reset to previous backup
        # erase the tex file with the backup and reload
        os.system('mv "' + self.filename + '.tex.bak" "' + self.filename + '.tex"')
        self.openFile(self.filename, self.page)
        # Re-init undo/redo stack
        self.undoStack = UndoStack(self)
      # else there is nothing to do,
      # the user need to fix the issue to be able to compile again
      # and get a preview of changes
    elif reloadAfterSave:
      # Case 1)
      msg.setText(
        self.tr(
          'The document could not be compiled and no backup of the TeX file was found. '
          'Fix the issue and retry to compile.' + f'\n\n{err}'
        )
      )
      msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
      answer = msg.exec_()
    else:
      # Case 2)
      msg.setText(
        self.tr(
          'The document could not be open in BEd (LaTeX compiling issue). '
          'You will have to fix the issue in an external editor '
          'and retry and open the document in BEd.'
        )
        + f'\n\n{err}'
      )
      msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
      answer = msg.exec_()
      self.filename = None
      self.document = None
      self.frame = None

  def _saveTeXandReload(self):
    """Save the current document in self.filename
    and reload it at page self.page
    """
    # self.filename and self.page must be defined
    self.document.writeTeX(self.filename + '.tex')
    # Re-load document from tex
    if settings.auto_reload:
      self.openFile(self.filename + '.tex', self.page, reloadAfterSave=True)
    # Remember that the saved version is the current one (see undo.py)
    self.undoStack.updateModified()

  def reloadTeX(self):
    """Reload current document from the last saved tex file"""
    if self.filename and self.checkSaved():
      self.openFile(self.filename + '.tex', self.page, reloadAfterSave=True)
      # Remember that the saved version is the current one (see undo.py)
      self.undoStack.updateModified()

  def previewCurrentFrame(self):
    """Compile and load current frame only"""
    if self.document:
      self.isCompiling = True
      self.painterArea.repaint()
      # Create tmp directory
      single_frame_dir_object = tempfile.TemporaryDirectory(prefix='bed-sfp-')
      single_frame_dir = single_frame_dir_object.name
      # Create tmp tex file with a single frame in it
      single_frame_file = single_frame_dir + '/preview.tex'
      self.document.writeTeX(single_frame_file, single_frame=self.frame)
      # Compile it (output to tmp directory)
      for _ in range(2):
        os.system(
          settings.latex_cmd
          + ' -output-directory="'
          + single_frame_dir
          + '"  "'
          + single_frame_file
          + '" | grep Error > '
          + self.compileOutput
        )
      # Check if the pdf has been produced and no errors have been detected
      if (
        os.path.isfile(single_frame_file[:-4] + '.pdf')
        and os.stat(self.compileOutput).st_size == 0
      ):
        # Load the compiled preview
        before = self.document.frames[self.frame].before
        firstpage = self.document.frames[self.frame].firstpage
        pdf = self.document.loadpdf(single_frame_file[:-4] + '.pdf')
        xmlDoc = parsing.parseall(single_frame_file[:-4])
        paper_w = float(xmlDoc.get('paper_w'))
        paper_h = float(xmlDoc.get('paper_h'))
        paper_ratio = paper_w / paper_h
        frame_npages = int(xmlDoc[0].get('n_pages'))
        if self.framePage >= frame_npages:
          dfpages = frame_npages - self.framePage - 1
          self.page += dfpages
          self.framePage += dfpages
        dnpages = frame_npages - self.document.frames[self.frame].npages
        self.document.frames[self.frame].readxml(xmlDoc[0], pdf, paper_ratio, paper_h)
        self.document.frames[self.frame].before = before
        self.document.frames[self.frame].firstpage = firstpage
        for fr in range(self.frame + 1, self.document.nframes):
          self.document.frames[fr].firstpage += dnpages
        self.document.npages += dnpages
        self.makePageList()
        self.makeFramePageList()
        self.setIndexes()
      else:
        QtWidgets.QApplication.restoreOverrideCursor()
        msg = QtWidgets.QMessageBox(self)
        msg.setIcon(QtWidgets.QMessageBox.Warning)
        msg.setWindowTitle(self.tr('LaTeX error detected'))
        with open(self.compileOutput) as cf:
          err = cf.read()
        msg.setText(
          self.tr(
            'The current frame could not be compiled. '
            'Fix the issue and retry to compile.'
          )
          + f'\n\n{err}'
        )
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msg.exec_()
      # Cleaning tmp directory
      single_frame_dir_object.cleanup()
      self.isCompiling = False
      self.painterArea.repaint()

  def save(self):
    """Save action
    To be called by saveAction.trigger.connect
    """
    if self.document:
      # If the filename is not defined then ask the user (save as...)
      if not self.filename:
        return self.saveAs()
      self._saveTeXandReload()
      # return whether the file has been saved
      return True
    return False

  def saveAs(self):
    """Dialog asking for a tex file to save current document
    To be called by saveAsAction.trigger.connect
    """
    if self.document:
      # Reset mouse cursor to default (remove resize, move... cursors)
      QtWidgets.QApplication.restoreOverrideCursor()
      filename = QtWidgets.QFileDialog.getSaveFileName(
        self, self.tr('Save File'), '.', 'TeX (*.tex)'
      )[0]
      if filename != '':
        # Separate folder and file
        spFolderFile = re.split(r'/', filename)
        folder = r'/'.join(spFolderFile[:-1])
        if folder == '':
          folder = os.getcwd()
        folder += '/'
        # Change working folder to the tex file folder
        os.chdir(folder)
        # Store current working path
        self.folder = folder
        # Separate filename and extension
        spNameExt = re.split(r'\.', spFolderFile[-1])
        if spNameExt[-1] == 'tex':
          self.filename = '.'.join(spNameExt[:-1])
        else:
          self.filename = spFolderFile[-1]
        # Save and reload
        self._saveTeXandReload()
        # Return wether the document has been saved
        return True
    return False

  def checkSaved(self):
    """Check if all changes have been saved in current document"""
    if not self.document or not self.modified:
      return True
    # There are unsaved changes
    # Show a dialog asking the user whether to save them
    # Reset mouse cursor to default (remove resize, move... cursors)
    QtWidgets.QApplication.restoreOverrideCursor()
    msg = QtWidgets.QMessageBox(self)
    msg.setIcon(QtWidgets.QMessageBox.Warning)
    msg.setWindowTitle(self.tr('Unsaved changes'))
    msg.setText(self.tr('Current document has been modified. Save modifications?'))
    msg.setStandardButtons(
      QtWidgets.QMessageBox.Save
      | QtWidgets.QMessageBox.Discard
      | QtWidgets.QMessageBox.Cancel
    )
    answer = msg.exec_()
    # Analyse the answer
    # If Cancel button, then checkSaved return false to warn the calling function
    if answer == QtWidgets.QMessageBox.Cancel:
      return False

    # # If the user ask for saving, launch saveFile
    # # If there is a problem with saving, return false to warn the calling function
    # # Otherwise (the file is saved or the user did not care) return True
    return answer != QtWidgets.QMessageBox.Save or self.save()
    #
    # # If the user ask for saving, launch saveFile
    # if answer == QtWidgets.QMessageBox.Save:
    #   if not self.save():
    #     # If there is a problem with saving, return false to warn the calling function
    #     return False
    # # Otherwise (the file is saved or the user did not care) return True
    # return True

  def closeEvent(self, event):
    """Things to do before closing app"""
    # Check if all changes to current document have been saved
    if self.checkSaved():
      # If its ok then write modified settings to the config file
      if settings.auto_save_settings:
        settings.write()
      # remove temp files
      if self.tmpFile:
        os.remove(self.tmpFile)
      if os.path.isfile(self.compileOutput):
        os.remove(self.compileOutput)
      # and close app
      event.accept()
    else:
      # If there are unsaved changed and the user canceled the closing process
      # then cancel it
      event.ignore()

  def makeFrameList(self):
    """Fill-in the combobox listing frames"""
    if self.document:
      # Remember that we are filling comboboxes
      # And that changes to them should not trigger actions
      self.fillingCombo = True
      self.frameCombo.clear()
      smxf = str(self.document.nframes)
      for f in range(self.document.nframes):
        self.frameCombo.addItem(str(f + 1) + r'/' + smxf)
      self.fillingCombo = False

  def makePageList(self):
    """Fill-in the combobox listing pages"""
    if self.document:
      # Remember that we are filling comboboxes
      # And that changes to them should not trigger actions
      self.fillingCombo = True
      self.pageCombo.clear()
      smxp = str(self.document.npages)
      for p in range(self.document.npages):
        self.pageCombo.addItem(str(p + 1) + r'/' + smxp)
      self.fillingCombo = False

  def makeFramePageList(self):
    """Fill-in the combobox listing framepages"""
    if self.document:
      # Remember that we are filling comboboxes
      # And that changes to them should not trigger actions
      self.fillingCombo = True
      self.framePageCombo.clear()
      smxfp = str(self.document.frames[self.frame].npages)
      for p in range(self.document.frames[self.frame].npages):
        self.framePageCombo.addItem(str(p + 1) + r'/' + smxfp)
      self.fillingCombo = False

  def setIndexes(self):
    """Set indexes in the three frame/page combobox
    to correspond to the current state (frame,page,framepage)
    """
    if self.document:
      # Remember that we are filling comboboxes
      # And that change to them should not trigger actions
      self.fillingCombo = True
      self.frameCombo.setCurrentIndex(self.frame)
      self.pageCombo.setCurrentIndex(self.page)
      self.framePageCombo.setCurrentIndex(self.framePage)
      self.fillingCombo = False

  def frameFromPage(self):
    """Compute self.frame and self.framePage from the value of self.page"""
    if self.document:
      # Simply browse the frame list from 0 until we reach the good one
      self.frame = 0
      while self.frame < self.document.nframes:
        self.framePage = self.page - self.document.frames[self.frame].firstpage
        if 0 <= self.framePage <= self.document.frames[self.frame].npages - 1:
          break
        self.frame += 1

  def previousPage(self):
    """Go to previous page"""
    if self.document and self.page > 0:
      # Check if the previous page is in the same frame or not
      # and adjust frame / framePage accordingly
      self.page -= 1
      if self.framePage > 0:
        self.framePage -= 1
      else:
        self.frame -= 1
        self.framePage = self.document.frames[self.frame].npages - 1
        # If the frame is different
        # The framePage combobox must be re-filled
        self.makeFramePageList()
      # Re-select the good indexes in the 3 frame/page comboboxes
      self.setIndexes()
      self.painterArea.repaint()

  def nextPage(self):
    """Go to next page"""
    # Check if the next page is in the same frame or not
    # and adjust frame / framePage accordingly
    if self.document and self.page < self.document.npages - 1:
      self.page += 1
      if self.framePage < self.document.frames[self.frame].npages - 1:
        self.framePage += 1
      else:
        self.frame += 1
        self.framePage = 0
        # If the frame is different
        # The framePage combobox must be re-filled
        self.makeFramePageList()
      # Re-select the good indexes in the 3 frame/page comboboxes
      self.setIndexes()
      self.painterArea.repaint()

  def changeFrame(self):
    """Frame change (triggered by a user change in the frame combobox)"""
    # Check if this is really the user
    # and not an actions triggered by the filling functions
    # Check if the user really changed something
    if not self.fillingCombo and self.frameCombo.currentIndex() != self.frame:
      # Get frame from selection in combobox
      self.frame = self.frameCombo.currentIndex()
      self.framePage = 0
      # Adjust page number
      self.page = self.document.frames[self.frame].firstpage
      # Re-fill framePage combobox
      self.makeFramePageList()
      # Re-select the good indexes in all comboboxes
      self.setIndexes()
      self.painterArea.repaint()

  def changePage(self):
    """Page change (triggered by a user change in the page combobox)"""
    # Check if this is really the user
    # and not an actions triggered by the filling functions
    # Check if the user really changed something
    if not self.fillingCombo and self.pageCombo.currentIndex() != self.page:
      # Get page from selection in combobox
      self.page = self.pageCombo.currentIndex()
      # Find the corresponding frame and see if it is different from the current one
      f = self.frame
      self.frameFromPage()
      if self.frame != f:
        # Re-fill the framePage combobox if the frame changed
        self.makeFramePageList()
      # Re-select the good indexes in all comboboxes
      self.setIndexes()
      self.painterArea.repaint()

  def changeFramePage(self):
    """FramePage change (triggered by a user change in the framePage combobox)"""
    # Check if this is really the user
    # and not an actions triggered by the filling functions
    # Check if the user really changed something
    if not self.fillingCombo and self.framePageCombo.currentIndex() != self.framePage:
      self.framePage = self.framePageCombo.currentIndex()
      # Compute new page
      self.page = self.document.frames[self.frame].firstpage + self.framePage
      # Re-select the good indexes in all comboboxes
      self.setIndexes()
      self.painterArea.repaint()

  def newFrame(self):
    """Insert a new frame just after the current one"""
    if self.document:
      # Add a temporary snapshot in the undo/redo stack
      # This snapshot can be confirmed (really put in the stack),
      # or canceled (completely forgotten)
      # if the user cancel the creation before the end of the creation process
      self.undoStack.doTemp()
      # Create the frame with default properties (from config file)
      newfr = Frame(
        settings.default_frame_title,
        [],
        [],
        [None],
        self.document.frames[self.frame].firstpage
        + self.document.frames[self.frame].npages,
        1,
      )
      # Adjust the page numbering of subsequent frames
      for f in range(self.frame + 1, self.document.nframes):
        self.document.frames[f].firstpage += 1
      # Adjust document total number of frames and pages
      self.document.nframes += 1
      self.document.npages += 1
      # Adjust currently selected frame to display the newly created one
      self.frame += 1
      # Insert the new frame at the right place in the document frame list
      self.document.frames.insert(self.frame, newfr)
      # Recompute the page number from frame (framePage is 0)
      self.framePage = 0
      self.page = self.document.frames[self.frame].firstpage
      # Re-fill frame/page comboboxes
      self.makeFrameList()
      self.makePageList()
      self.makeFramePageList()
      # Re-select the good indexes for all combobox
      self.setIndexes()
      self.painterArea.repaint()
      # Edit the newly created frame properties (edit dialog)
      self.editAny(new=True)

  def newFrameTemplate(self, templateID):
    """Insert a new frame just after the current one"""
    if self.document:
      # Add a snapshot in the undo/redo stack
      self.undoStack.doTemp()
      try:
        # Create the frame from the template
        spbf = settings.templates[2 * templateID + 1].split('\\begin{frame}')
        before = spbf[0]
        title = spbf[1].split('\\end{frame}')[0]
        newfr = Frame(
          title,
          [],
          [],
          [None],
          self.document.frames[self.frame].firstpage
          + self.document.frames[self.frame].npages,
          1,
          before,
        )
        # Adjust the page numbering of subsequent frames
        for f in range(self.frame + 1, self.document.nframes):
          self.document.frames[f].firstpage += 1
        # Adjust document total number of frames and pages
        self.document.nframes += 1
        self.document.npages += 1
        # Adjust currently selected frame to display the newly created one
        self.frame += 1
        # Insert the new frame at the right place in the document frame list
        self.document.frames.insert(self.frame, newfr)
        # Recompute the page number from frame (framePage is 0)
        self.framePage = 0
        self.page = self.document.frames[self.frame].firstpage
        # Re-fill frame/page comboboxes
        self.makeFrameList()
        self.makePageList()
        self.makeFramePageList()
        # Re-select the good indexes for all combobox
        self.setIndexes()
        self.previewCurrentFrame()
        self.undoStack.confirmTemp()
      except Exception as e:
        print(e)
        self.undoStack.reloadTemp()

  def saveTemplate(self):
    """Save the current frame as a template"""
    if self.document and self.document.nframes > 0:
      # Ask for a name
      QtWidgets.QApplication.restoreOverrideCursor()
      dialog = QtWidgets.QInputDialog(self, QtCore.Qt.Tool)
      dialog.setWindowTitle(self.tr('New template'))
      dialog.setLabelText(self.tr('Template name'))
      dialog.setTextValue(self.tr('Template') + f' {len(settings.templates) // 2 + 1}')
      dialog.resize(300, dialog.height())
      ok = dialog.exec_()
      if ok:
        settings.templates.extend(
          [dialog.textValue(), striplines(self.document.frames[self.frame].writeTeX())]
        )
        # Re-init UI to update templates menu
        self.resetUI()

  def deleteTemplate(self):
    """Delete one of the saved templates"""
    if settings.templates != []:
      # Ask which templates should be deleted
      QtWidgets.QApplication.restoreOverrideCursor()
      dialog = QtWidgets.QInputDialog(self, QtCore.Qt.Tool)
      dialog.setWindowTitle(self.tr('Delete template'))
      dialog.setLabelText(self.tr('Template name'))
      dialog.setComboBoxItems(settings.templates[::2])
      dialog.resize(300, dialog.height())
      ok = dialog.exec_()
      if ok:
        index = settings.templates.index(dialog.textValue())
        settings.templates.pop(index)
        settings.templates.pop(index)
        self.resetUI()

  def newText(self):
    """Insert a new text in the current frame"""
    if self.document:
      # Add a temporary snapshot in the undo/redo stack
      # This snapshot can be confirmed (really put in the stack),
      # or canceled (completely forgotten)
      # if the user cancel the creation before the end of the creation process
      self.undoStack.doTemp()
      # Unselect any currently selected object in the frame
      for gel in (
        self.document.frames[self.frame].elements
        + self.document.frames[self.frame].groups
      ):
        gel.selected = False
      # By default the new text will appear in all pages of the frame (framePages)
      pages = []
      for p in range(self.document.frames[self.frame].npages):
        pages.append(p)
      # Create the new text with default properties (from config file)
      text = Text(
        settings.default_text_x,
        settings.default_text_y,
        settings.default_text_w,
        settings.default_text_h,
        minh=settings.default_text_h,
        text=settings.default_text_text,
        pagesList=pages,
        selected=True,
        paper_ratio=self.document.paper_ratio,
      )
      # Add it at the end of the frame element list
      self.document.frames[self.frame].elements.append(text)
      self.painterArea.repaint()
      # Edit the newly created text properties (edit dialog)
      self.editAny(new=True)

  def newImage(self):
    """Insert a new image in the current frame"""
    if self.document:
      # Add a temporary snapshot in the undo/redo stack
      # This snapshot can be confirmed (really put in the stack),
      # or canceled (completely forgotten)
      # if the user cancel the creation before the end of the creation process
      self.undoStack.doTemp()
      # Unselect any currently selected object in the frame
      for gel in (
        self.document.frames[self.frame].elements
        + self.document.frames[self.frame].groups
      ):
        gel.selected = False
      # By default the new image will appear in all pages of the frame (framePages)
      pages = []
      for p in range(self.document.frames[self.frame].npages):
        pages.append(p)
      # Create the new image with default properties (from config file)
      image = Image(
        settings.default_image_x,
        settings.default_image_y,
        settings.default_image_w,
        settings.default_image_h,
        pagesList=pages,
        selected=True,
        paper_ratio=self.document.paper_ratio,
      )
      # Add it at the end of the frame element list
      self.document.frames[self.frame].elements.append(image)
      self.painterArea.repaint()
      # Edit the newly created image properties (edit dialog)
      self.editAny(new=True)

  def newTikzPicture(self):
    """Insert a new Tikz picture in the current frame"""
    if self.document:
      # Add a temporary snapshot in the undo/redo stack
      # This snapshot can be confirmed (really put in the stack),
      # or canceled (completely forgotten)
      # if the user cancel the creation before the end of the creation process
      self.undoStack.doTemp()
      # Unselect any currently selected object in the frame
      for gel in (
        self.document.frames[self.frame].elements
        + self.document.frames[self.frame].groups
      ):
        gel.selected = False
      # By default the new image will appear in all pages of the frame (framePages)
      pages = []
      for p in range(self.document.frames[self.frame].npages):
        pages.append(p)
      # Create the new image with default properties (from config file)
      tikzpic = TikzPicture(
        settings.default_tikzpicture_x,
        settings.default_tikzpicture_y,
        settings.default_tikzpicture_w,
        settings.default_tikzpicture_h,
        pagesList=pages,
        selected=True,
        paper_ratio=self.document.paper_ratio,
        tikzcmd=settings.default_tikzpicture_cmd,
      )
      # Add it at the end of the frame element list
      self.document.frames[self.frame].elements.append(tikzpic)
      self.painterArea.repaint()
      # Edit the newly created Tikz picture properties (edit dialog)
      self.editAny(new=True)

  def newArrow(self):
    """Insert a new arrow in the current frame"""
    if self.document:
      # Add a temporary snapshot in the undo/redo stack
      # This snapshot can be confirmed (really put in the stack),
      # or canceled (completely forgotten)
      # if the user cancel the creation before the end of the creation process
      self.undoStack.doTemp()
      # Unselect any currently selected object in the frame
      for gel in (
        self.document.frames[self.frame].elements
        + self.document.frames[self.frame].groups
      ):
        gel.selected = False
      # By default the new arrow will appear in all pages of the frame (framePages)
      pages = []
      for p in range(self.document.frames[self.frame].npages):
        pages.append(p)
      # Create the new arrow with default properties (from config file)
      h = settings.default_arrow_lw / self.document.paper_h
      arrow = Arrow(
        settings.default_arrow_x,
        settings.default_arrow_y - h / 2,
        settings.default_arrow_w,
        h,
        pagesList=pages,
        selected=True,
        paper_ratio=self.document.paper_ratio,
        paper_h=self.document.paper_h,
        opt=settings.default_arrow_opt,
      )
      # Add it at the end of the frame element list
      self.document.frames[self.frame].elements.append(arrow)
      self.painterArea.repaint()
      # Edit the newly created arrow properties (edit dialog)
      self.editAny(new=True)

  def group(self):
    """Group selected elements"""
    if self.document:
      # Add a snapshot in the undo/redo stack
      self.undoStack.do()
      # Call the group function of the current frame
      self.document.frames[self.frame].group(self.document.paper_ratio)
    self.painterArea.repaint()

  def ungroup(self):
    """Ungroup selected elements"""
    if self.document:
      # Add a snapshot in the undo/redo stack
      self.undoStack.do()
      # Call the ungroup function of the current frame
      self.document.frames[self.frame].ungroup()
    self.painterArea.repaint()

  def deleteAny(self):
    """Delete selected elements in the current frame
    If nothing is selected, delete the frame
    """
    if self.document:
      # Add a snapshot in the undo/redo stack
      self.undoStack.do()
      # Browse the frame elements/groups
      # To remove selected ones
      # found is True if something is selected
      found = False
      # Reverse the list to be able to remove selected elements
      # without perturbing the for loop
      for el in reversed(self.document.frames[self.frame].elements):
        if el.selected:
          found = True
          self.document.frames[self.frame].elements.remove(el)
      # Reverse the list to be able to remove selected groups
      # without perturbing the for loop
      for g in reversed(self.document.frames[self.frame].groups):
        if g.selected:
          found = True
          for el in g.elements:
            self.document.frames[self.frame].elements.remove(el)
          self.document.frames[self.frame].groups.remove(g)
      # If nothing was selected then the whole frame must be removed from the document
      # Except if it is the only frame (avoid problems)
      if not found and self.document.nframes > 1:
        # Re-adjust the page numberings of subsequent frames
        for f in range(self.frame + 1, self.document.nframes):
          self.document.frames[f].firstpage -= self.document.frames[self.frame].npages
        # Re-adjust the document page and frame numbers
        self.document.npages -= self.document.frames[self.frame].npages
        self.document.nframes -= 1
        # Remove the frame
        del self.document.frames[self.frame]
        # Go to the next frame (first framePage)
        # Except if it was the last frame
        # (in this case go to the previous one, last framePage)
        if self.frame == self.document.nframes:
          self.frame -= 1
          self.framePage = self.document.frames[self.frame].npages - 1
          self.page = self.document.frames[self.frame].firstpage + self.framePage
        else:
          self.framePage = 0
          self.page = self.document.frames[self.frame].firstpage
        # Re-fill comboboxes
        self.makeFrameList()
        self.makePageList()
        self.makeFramePageList()
        # Re-select good indexes in comboboxes
        self.setIndexes()
      self.painterArea.repaint()

  def copyAny(self):
    """Just a version of copyCutAny without args
    To be called by copyAction.trigger.connect
    """
    self.copyCutAny()

  def cutAny(self):
    """Just a version of copyCutAny with a True argument
    To be called by cutAction.trigger.connect
    """
    self.copyCutAny(True)

  def copyCutAny(self, cut=False):
    """Copy or cut selected elements/groups
    If nothing is selected copy or cut the whole frame
    """
    # Init the list of copied elements/groups
    self.copyList = []
    if self.document:
      # Find selected elements and put copies of them in the copyList
      for gel in (
        self.document.frames[self.frame].elements
        + self.document.frames[self.frame].groups
      ):
        if gel.selected:
          self.copyList.append(gel.copy())
      # If nothing was selected, copy the whole frame (and put it in the copyList)
      if self.copyList == []:
        self.copyList = self.document.frames[self.frame].copy()
      # If cut is asked, them remove the selected elements
      if cut:
        self.deleteAny()

  def pasteAny(self):
    """Paste elements/groups/frames contained in the copyList"""
    if self.document:
      # Add a snapshot in the undo/redo stack
      self.undoStack.do()
      # Check if the copyList is a list of elements/groups or a whole frame
      if type(self.copyList) is Frame:
        # insert the frame just after the current one
        self.copyList.firstpage = (
          self.document.frames[self.frame].firstpage
          + self.document.frames[self.frame].npages
        )
        for f in range(self.frame + 1, self.document.nframes):
          self.document.frames[f].firstpage += self.copyList.npages
        self.frame += 1
        self.document.nframes += 1
        self.document.npages += self.copyList.npages
        self.document.frames.insert(self.frame, self.copyList)
        self.page = self.document.frames[self.frame].firstpage
        self.framePage = 0
        self.makeFrameList()
        self.makePageList()
        self.makeFramePageList()
        self.setIndexes()
      else:
        # Unselect any selected object in the current slide
        # before copying elements/groups
        for obj in (
          self.document.frames[self.frame].elements
          + self.document.frames[self.frame].groups
        ):
          obj.selected = False
        # Copy each element of the copyList
        for obj in self.copyList:
          # Create a copy of the object (in order to be able to copy it several times)
          cobj = obj.copy()
          if type(obj) is Group:
            # If the copied object is a group
            # add the object to the frame groups list
            # AND add all the contained elements to the current frame elements list
            self.document.frames[self.frame].groups.append(cobj)
            for el in cobj.elements:
              self.document.frames[self.frame].elements.append(el)
          else:
            # If it is a single element
            # just add it to the frame elements list
            self.document.frames[self.frame].elements.append(cobj)
      self.painterArea.repaint()

  def editAnyConnect(self):
    """Just a version of editAny without args
    To be called by editAction.trigger.connect
    """
    self.editAny()

  def editAny(self, new=False):
    """Edit the selected elements/groups one by one
    If nothing is selected, edit the current frame (frame title)
    """
    if self.document:
      if not new:
        # If the element has not just been created
        # add a temporary snapshot in the undo/redo stack
        # This snapshot can be confirmed (really put in the stack),
        # or canceled (completely forgotten)
        # if the user does not really edit anything
        self.undoStack.doTemp()
      found = False
      validate = False
      for gel in (
        self.document.frames[self.frame].elements
        + self.document.frames[self.frame].groups
      ):
        if gel.selected:
          # if the element/group is selected
          # launch the edit dialog for it
          validate = validate or gel.edit(self)
          found = True
      # If nothing was selected
      # launch the frame edit dialog
      if not found:
        validate = self.document.frames[self.frame].edit(self)
      if validate:
        self.undoStack.confirmTemp()
        self.painterArea.repaint()
      else:
        self.undoStack.reloadTemp()

  def editDoc(self):
    """Edit the document properties (header/footer of tex file)"""
    if self.document:
      # Add a temporary snapshot in the undo/redo stack
      # This snapshot can be confirmed (really put in the stack),
      # or canceled (completely forgotten)
      # if the user does not really edit anything
      self.undoStack.doTemp()
      if self.document.edit(self):
        self.undoStack.confirmTemp()
        self.painterArea.repaint()
      else:
        self.undoStack.reloadTemp()

  def moveUp(self):
    """Move the selected elements/groups one notch up (toward foreground)"""
    # Of course, if a selected element is already at the top, we do nothing
    # One difficulty here is that if the two top elements are selected
    # we must not put the second one on top of the first one
    # indE keep track of this kind of pb
    # If a group is selected, all the contained elements will also be moved up
    # Note that foreground correspond to the end of the lists (last drawn)
    if self.document:
      # Add a snapshot in the undo/redo stack
      self.undoStack.do()
      # Look for selected elements (or elements of selected groups)
      indE = 0
      # Reverse lists to treat top elements first
      for cind, el in enumerate(reversed(self.document.frames[self.frame].elements)):
        # compute the index in list from the index in reversed list
        ind = len(self.document.frames[self.frame].elements) - 1 - cind
        if el.selected or (el.group and el.group.selected):
          # Check if it is possible to put the element up
          if cind > indE:
            # do it by swapping the element with the next one in list
            (
              self.document.frames[self.frame].elements[ind],
              self.document.frames[self.frame].elements[ind + 1],
            ) = (
              self.document.frames[self.frame].elements[ind + 1],
              self.document.frames[self.frame].elements[ind],
            )
          indE += 1
      # If nothing was selected move the current frame up (swap with previous one)
      if indE == 0 and self.frame > 0:
        self.document.frames[self.frame].firstpage -= self.document.frames[
          self.frame - 1
        ].npages
        self.document.frames[self.frame - 1].firstpage += self.document.frames[
          self.frame
        ].npages
        self.page -= self.document.frames[self.frame - 1].npages
        self.document.frames[self.frame], self.document.frames[self.frame - 1] = (
          self.document.frames[self.frame - 1],
          self.document.frames[self.frame],
        )
        self.frame -= 1
        self.setIndexes()
      self.painterArea.repaint()

  def moveDown(self):
    """Move the selected elements/groups one notch down (toward background)"""
    # See initial comment in moveUp
    if self.document:
      # Add a snapshot in the undo/redo stack
      self.undoStack.do()
      # Look for selected elements (or elements of selected groups)
      indE = 0
      for ind, el in enumerate(self.document.frames[self.frame].elements):
        if el.selected or (el.group and el.group.selected):
          # Check if it is possible to put the element down
          if ind > indE:
            # do it by swapping the element with the previous one in list
            (
              self.document.frames[self.frame].elements[ind],
              self.document.frames[self.frame].elements[ind - 1],
            ) = (
              self.document.frames[self.frame].elements[ind - 1],
              self.document.frames[self.frame].elements[ind],
            )
          indE += 1
      # If nothing was selected move the current frame down (swap with next one)
      if indE == 0 and self.frame < self.document.nframes - 1:
        self.document.frames[self.frame].firstpage += self.document.frames[
          self.frame + 1
        ].npages
        self.document.frames[self.frame + 1].firstpage -= self.document.frames[
          self.frame
        ].npages
        self.page += self.document.frames[self.frame + 1].npages
        self.document.frames[self.frame], self.document.frames[self.frame + 1] = (
          self.document.frames[self.frame + 1],
          self.document.frames[self.frame],
        )
        self.frame += 1
        self.setIndexes()
      self.painterArea.repaint()

  def moveTop(self):
    """Move the selected elements/groups to top (toward foreground)"""
    # Same as moveUp but with while loops instead of if statements
    if self.document:
      self.undoStack.do()
      indE = 0
      for tcind, el in enumerate(reversed(self.document.frames[self.frame].elements)):
        # make a copy of the index since we will affect it in the while loop
        cind = tcind
        ind = len(self.document.frames[self.frame].elements) - 1 - cind
        if el.selected or (el.group and el.group.selected):
          while cind > indE:
            (
              self.document.frames[self.frame].elements[ind],
              self.document.frames[self.frame].elements[ind + 1],
            ) = (
              self.document.frames[self.frame].elements[ind + 1],
              self.document.frames[self.frame].elements[ind],
            )
            ind += 1
            cind -= 1
          indE += 1
      if indE == 0:
        while self.frame > 0:
          self.document.frames[self.frame].firstpage -= self.document.frames[
            self.frame - 1
          ].npages
          self.document.frames[self.frame - 1].firstpage += self.document.frames[
            self.frame
          ].npages
          self.page -= self.document.frames[self.frame - 1].npages
          self.document.frames[self.frame], self.document.frames[self.frame - 1] = (
            self.document.frames[self.frame - 1],
            self.document.frames[self.frame],
          )
          self.frame -= 1
        self.setIndexes()
      self.painterArea.repaint()

  def moveBottom(self):
    """Move the selected elements/groups one notch down (toward background)"""
    # Same as moveDown but with while loops instead of if statements
    if self.document:
      self.undoStack.do()
      indE = 0
      for tind, el in enumerate(self.document.frames[self.frame].elements):
        # make a copy of the index since we will affect it in the while loop
        ind = tind
        if el.selected or (el.group and el.group.selected):
          while ind > indE:
            (
              self.document.frames[self.frame].elements[ind],
              self.document.frames[self.frame].elements[ind - 1],
            ) = (
              self.document.frames[self.frame].elements[ind - 1],
              self.document.frames[self.frame].elements[ind],
            )
            ind -= 1
          indE += 1

      if indE == 0:
        while self.frame < self.document.nframes - 1:
          self.document.frames[self.frame].firstpage += self.document.frames[
            self.frame + 1
          ].npages
          self.document.frames[self.frame + 1].firstpage -= self.document.frames[
            self.frame
          ].npages
          self.page += self.document.frames[self.frame + 1].npages
          self.document.frames[self.frame], self.document.frames[self.frame + 1] = (
            self.document.frames[self.frame + 1],
            self.document.frames[self.frame],
          )
          self.frame += 1
        self.setIndexes()
      self.painterArea.repaint()

  def undo(self):
    """Undo function"""
    # This is only an intermediate function
    # the real one is implemented in undo.py (undoStack class)
    # This is used to be able to load the ui before defining the undoStack
    if self.document:
      self.undoStack.undo()

  def redo(self):
    """Redo function"""
    # This is only an intermediate function
    # the real one is implemented in undo.py (undoStack class)
    # This is used to be able to load the ui before defining the undoStack
    if self.document:
      self.undoStack.redo()

  def toggleGrid(self):
    """Show/hide the grid and activate/deactivate grid magnetism"""
    # Get the state from the activateGridAction check state
    settings.activate_grid = self.activateGridAction.isChecked()
    self.painterArea.repaint()

  def toggleObjGuides(self):
    """Show/hide the objects guides and activate/deactivate objects magnetism"""
    # Get the state from the activateObjGuidesAction check state
    settings.activate_object_guides = self.activateObjGuidesAction.isChecked()
    self.painterArea.repaint()

  def toggleHiddenObjects(self):
    """Show/hide the hidden objects in the page"""
    # Get the state from the showHiddenObjectsAction check state
    settings.show_hidden_objects = self.showHiddenObjectsAction.isChecked()
    self.painterArea.repaint()

  def toggleMenu(self):
    """Show/hide menubar"""
    # Get the state from the hideMenuAction check state
    settings.menuVisible = self.hideMenuAction.isChecked()
    # Set visibility accordingly
    self.menu.setVisible(settings.menuVisible)

  def togglePagebar(self, visible):
    """Show/hide Pagebar"""
    # Save visibility in settings
    settings.pagebarVisible = visible

  def editSettings(self):
    if settings.edit(self):
      # Re-init UI in case some properties changed
      self.resetUI()

  def toggleAutoSaveSettings(self):
    """Switch on/off auto-save settings on application closing"""
    # Get the state from the autoSaveSettingsAction check state
    settings.auto_save_settings = self.autoSaveSettingsAction.isChecked()

  def errorHandler(self, *args):
    """Show the error and useful info in a message box when an exception is raised"""
    traceback.print_last()
    QtWidgets.QApplication.restoreOverrideCursor()
    msg = QtWidgets.QMessageBox(self)
    msg.setIcon(QtWidgets.QMessageBox.Critical)
    msg.setWindowTitle(self.tr('BEd error'))
    text = self.tr('The following error was detected:')
    trb = '\n'.join(traceback.format_exception(*args))
    text += '<pre>' + html.escape(f'\n{trb}\n') + '</pre>'
    text += self.tr('Try to save your document and restart BEd.')
    text += '<br><br>' + self.tr('Please consider filling a bug report at:')
    text += '<br><a href="https://framagit.org/delisle/bed/-/issues">https://framagit.org/delisle/bed/-/issues</a>'
    msg.setText(text)
    msg.setTextFormat(QtCore.Qt.RichText)
    msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
    msg.exec_()


def main():
  # Make sure latex will find bed.sty
  if os.system('kpsewhich bed.sty'):  # detects error codes (returns non-zero value)
    os.environ['TEXINPUTS'] = f'{os.environ.get("TEXINPUTS","")}:{_latex_path}'
  # Initialise app
  app = QtWidgets.QApplication(sys.argv)
  app.setApplicationName('BEd')
  app.setApplicationDisplayName('BEd')
  app.setDesktopFileName('bed')
  # Get the system language to load translator files
  lang = QtCore.QLocale().system().name().split('_')[0]
  translator = QtCore.QTranslator()
  translator.load(f'{lang}.qm', _tr_path)
  app.installTranslator(translator)
  bed = BEd()
  sys.excepthook = bed.errorHandler

  # Check if optionnal arguments are passed (filename, pagenumber)
  def initdoc():
    if len(sys.argv) > 2:
      bed.initDocument(sys.argv[1], int(sys.argv[2]) - 1)
    elif len(sys.argv) > 1:
      bed.initDocument(sys.argv[1])
    else:
      bed.initDocument()

  # Launch initdoc after application (wait 100 ms)
  QtCore.QTimer.singleShot(100, initdoc)
  sys.exit(app.exec_())

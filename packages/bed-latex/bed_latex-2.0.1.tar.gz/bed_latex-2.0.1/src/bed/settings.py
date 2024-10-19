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

# This file defines the Settings class, that deals with the application settings
# (based on QtCore.QSettings)

from collections import OrderedDict

from PySide6 import QtCore, QtGui

from .editor import (
  BedAdjustTextEdit,
  BedCheckBox,
  BedColorPicker,
  BedDoubleSpinBox,
  BedPenPicker,
  BedSpinBox,
  PropertiesEditor,
)


class Settings:
  def load(self, orgname, name):
    """Initialisation"""
    self._settings = QtCore.QSettings(orgname, name)
    # Read config file
    self.init()
    self.read()

  def tr(self, sourceText, disambiguation=''):
    return QtCore.QCoreApplication.translate('Settings', sourceText, disambiguation)

  def readkey(self, key, default=False):
    """Read the value of the setting named key"""
    # If default is True, return the default value of the setting
    # Use a dummy key to avoid getting the current value
    keyb = 'invalid_key' if default else key
    # Check type of expected value and convert the result to it
    if self._types[key] == QtGui.QColor:
      return QtGui.QColor(self._settings.value(keyb, self._defaults[key].name(), str))
    if self._types[key] == QtGui.QPen:
      penstr = self._settings.value(
        keyb,
        self._defaults[key].color().name() + ',' + str(self._defaults[key].widthF()),
        str,
      ).split(',')
      return QtGui.QPen(QtGui.QColor(penstr[0]), float(penstr[1]))
    return self._settings.value(keyb, self._defaults[key], self._types[key])

  def read(self):
    """Load settings from the config file"""
    for key in self._defaults:
      self.__dict__[key] = self.readkey(key)

  def write(self):
    """Write current settings in the config file"""
    for key in self._defaults:
      if self.__dict__[key] != self.readkey(key, True):
        if self._types[key] == QtGui.QColor:
          self._settings.setValue(key, self.__dict__[key].name())
        elif self._types[key] == QtGui.QPen:
          self._settings.setValue(
            key,
            self.__dict__[key].color().name() + ',' + str(self.__dict__[key].widthF()),
          )
        else:
          self._settings.setValue(key, self.__dict__[key])
      else:
        self._settings.remove(key)

  def edit(self, parentwindow):
    # List all the possible settings that can be changed
    keys = []
    initvalues = []
    bedwidgets = []
    # Sort the keys in alphabetical order
    for key in self._defaults:
      if key not in self._descriptions:
        # Hide undescribed settings.
        continue
      keys.append(key)
      # Select widget depending on type
      if self._types[key] is int:
        initvalues.append(self.__dict__[key])
        bedwidgets.append(
          BedSpinBox(
            initvalues[-1],
            0,
            10000,
            1,
            label=self._descriptions[key],
            default=self._defaults[key],
            parent=parentwindow,
          )
        )
      elif self._types[key] is float:
        initvalues.append(self.__dict__[key])
        bedwidgets.append(
          BedDoubleSpinBox(
            initvalues[-1],
            -2,
            10000,
            0.1,
            5,
            label=self._descriptions[key],
            default=self._defaults[key],
            parent=parentwindow,
          )
        )
      elif self._types[key] is bool:
        initvalues.append(self.__dict__[key])
        bedwidgets.append(
          BedCheckBox(
            initvalues[-1],
            label=self._descriptions[key],
            default=self._defaults[key],
            parent=parentwindow,
          )
        )
      elif self._types[key] is QtGui.QColor:
        initvalues.append(self.__dict__[key])
        bedwidgets.append(
          BedColorPicker(
            initvalues[-1],
            label=self._descriptions[key],
            default=self._defaults[key],
            parent=parentwindow,
          )
        )
      elif self._types[key] is QtGui.QPen:
        initvalues.append(self.__dict__[key])
        bedwidgets.append(
          BedPenPicker(
            initvalues[-1],
            label=self._descriptions[key],
            default=self._defaults[key],
            parent=parentwindow,
          )
        )
      else:
        initvalues.append(str(self.__dict__[key]))
        highlight = self._highlights.get(key, False)
        bedwidgets.append(
          BedAdjustTextEdit(
            initvalues[-1],
            label=self._descriptions[key],
            default=str(self._defaults[key]),
            parent=parentwindow,
            highlight=highlight,
          )
        )
    # Get the values from user
    values = PropertiesEditor.getValues(
      parentwindow, bedwidgets, self, 'settings', self.tr('Settings')
    )
    if values:
      # Apply changes
      for key, v, iv in zip(keys, values, initvalues):
        if v != iv:
          self.__dict__[key] = eval(v) if self._types[key] is list else v
      return True
    return False

  def init(self):
    """Initialisation of the defaults and types dictionnaries
    with all the key, default value and types.
    """
    self._descriptions = OrderedDict()
    self._types = OrderedDict()
    self._defaults = OrderedDict()
    self._highlights = OrderedDict()

    # Important settings
    self._descriptions['latex_cmd'] = self.tr('LaTeX command')
    self._defaults['latex_cmd'] = 'pdflatex -interaction=nonstopmode'
    self._types['latex_cmd'] = str
    self._descriptions['indent_cmd'] = self.tr('Indenting command')
    self._defaults['indent_cmd'] = ''
    self._types['indent_cmd'] = str
    self._descriptions['dpi'] = self.tr('Display resolution (dpi)')
    self._defaults['dpi'] = 300
    self._types['dpi'] = int
    self._descriptions['auto_reload'] = self.tr(
      'Automatically reload document when saving'
    )
    self._defaults['auto_reload'] = True
    self._types['auto_reload'] = bool
    self._descriptions['Nkeep_previews'] = self.tr(
      'Number of previews kept in undo stack'
    )
    self._defaults['Nkeep_previews'] = 4
    self._types['Nkeep_previews'] = int
    self._descriptions['Ngrid'] = self.tr('Number of lines in grid')
    self._defaults['Ngrid'] = 80
    self._types['Ngrid'] = int

    self._descriptions['epsilon'] = self.tr('Rounding precision')
    self._defaults['epsilon'] = 1e-4
    self._types['epsilon'] = float

    # Default contents/objects properties
    self._descriptions['default_header'] = self.tr('Default LaTeX header')
    self._defaults['default_header'] = (
      '\\documentclass[12pt]{beamer}\n\\usepackage{bed}\n\\usepackage[T1]{fontenc}\n'
      '\\usepackage[utf8]{inputenc}\n\\usefonttheme{professionalfonts}\n'
      '\\usepackage{amsmath}\n\\usepackage{amsthm}\n\\usepackage{mathtools}\n'
      '\\usepackage[varg]{txfonts} % times font\n'
      '\\usepackage{grffile} % Accept filenames with dots for images\n'
      '\n% Document infos\n\\title[running title]{Title}\n'
      '\\author[running author]{Author}\n\\institute[running inst.]{Institute}\n'
      '\\date{\\today}\n\n% Beamer theme\n'
      '\\usetheme{Madrid}\n\\usecolortheme{beaver}\n\n'
      '% Commands for bullets...\n'
      '\\newcommand{\\bull}[1]{{\\color{#1}\\textbullet}\\hspace{\\labelsep}\\!\\!}\n'
      '\\newcommand{\\dash}[1]{{\\color{#1}--}\\hspace{\\labelsep}\\!\\!}\n'
      '\\setbeamertemplate{itemize item}{{\\color{blue}\\textbullet}}\n'
      '\\settowidth{\\leftmargini}{\\usebeamertemplate{itemize item}'
      '\\hspace{-\\labelsep}\\hspace{0.0625\\paperwidth}}\n'
      '\\setbeamertemplate{itemize subitem}{{\\color{blue}--}}\n'
      '\\setbeamertemplate{enumerate items}[circle]\n'
      '\\beamertemplatenavigationsymbolsempty\n\n\\begin{document}'
    )
    self._types['default_header'] = str
    self._highlights['default_header'] = True
    self._descriptions['default_footer'] = self.tr('Default LaTeX footer')
    self._defaults['default_footer'] = '\\end{document}'
    self._types['default_footer'] = str
    self._highlights['default_footer'] = True
    self._descriptions['default_newdoc_frame_title'] = self.tr(
      'Default title page content'
    )
    self._defaults['default_newdoc_frame_title'] = '[plain]\n\\titlepage'
    self._types['default_newdoc_frame_title'] = str
    self._highlights['default_newdoc_frame_title'] = True
    self._descriptions['default_frame_title'] = self.tr('Default frame title')
    self._defaults['default_frame_title'] = '{New Frame}'
    self._types['default_frame_title'] = str
    self._highlights['default_frame_title'] = True
    self._descriptions['default_text_x'] = self.tr('Text [Default x]')
    self._defaults['default_text_x'] = 0.0625
    self._types['default_text_x'] = float
    self._descriptions['default_text_y'] = self.tr('Text [Default y]')
    self._defaults['default_text_y'] = 0.125
    self._types['default_text_y'] = float
    self._descriptions['default_text_w'] = self.tr('Text [Default width]')
    self._defaults['default_text_w'] = 0.875
    self._types['default_text_w'] = float
    self._descriptions['default_text_h'] = self.tr('Text [Default height]')
    self._defaults['default_text_h'] = 0.0375
    self._types['default_text_h'] = float
    self._descriptions['default_text_text'] = self.tr('Text [Default text]')
    self._defaults['default_text_text'] = '\\bull{blue} Text'
    self._types['default_text_text'] = str
    self._highlights['default_text_text'] = True
    self._descriptions['default_image_x'] = self.tr('Image [Default x]')
    self._defaults['default_image_x'] = 0.25
    self._types['default_image_x'] = float
    self._descriptions['default_image_y'] = self.tr('Image [Default y]')
    self._defaults['default_image_y'] = 0.25
    self._types['default_image_y'] = float
    self._descriptions['default_image_w'] = self.tr('Image [Default width]')
    self._defaults['default_image_w'] = 0.5
    self._types['default_image_w'] = float
    self._descriptions['default_image_h'] = self.tr('Image [Default height]')
    self._defaults['default_image_h'] = 0.5
    self._types['default_image_h'] = float
    self._descriptions['default_tikzpicture_x'] = self.tr('Tikz picture [Default x]')
    self._defaults['default_tikzpicture_x'] = 0.3125
    self._types['default_tikzpicture_x'] = float
    self._descriptions['default_tikzpicture_y'] = self.tr('Tikz picture [Default y]')
    self._defaults['default_tikzpicture_y'] = 0.25
    self._types['default_tikzpicture_y'] = float
    self._descriptions['default_tikzpicture_w'] = self.tr(
      'Tikz picture [Default width]'
    )
    self._defaults['default_tikzpicture_w'] = 0.375
    self._types['default_tikzpicture_w'] = float
    self._descriptions['default_tikzpicture_h'] = self.tr(
      'Tikz picture [Default height]'
    )
    self._defaults['default_tikzpicture_h'] = 0.5
    self._types['default_tikzpicture_h'] = float
    self._descriptions['default_tikzpicture_cmd'] = self.tr(
      'Tikz picture [Default command]'
    )
    self._defaults['default_tikzpicture_cmd'] = (
      '\\clip (-0.15,-0.35) rectangle (0.95,0.75);\n'
      '\\fill[red] (0,0) rectangle (0.8,0.2);\n'
      '\\fill[red] (-0.1,-0.2) -- (-0.1,0.5) arc (180:0:0.075) -- (0.05,-0.2);\n'
      '\\fill[red] (0.75,-0.2) -- (0.75,0.25) arc (180:0:0.075) -- (0.9,-0.2);\n'
      '\\fill[red] (0,0) -- (90:0.4) arc (90:0:0.4);'
    )
    self._types['default_tikzpicture_cmd'] = str
    self._highlights['default_tikzpicture_cmd'] = True
    self._descriptions['default_arrow_x'] = self.tr('Arrow [Default x]')
    self._defaults['default_arrow_x'] = 0.4
    self._types['default_arrow_x'] = float
    self._descriptions['default_arrow_y'] = self.tr('Arrow [Default y]')
    self._defaults['default_arrow_y'] = 0.5
    self._types['default_arrow_y'] = float
    self._descriptions['default_arrow_w'] = self.tr('Arrow [Default width]')
    self._defaults['default_arrow_w'] = 0.2
    self._types['default_arrow_w'] = float
    self._descriptions['default_arrow_lw'] = self.tr('Arrow [Default line width]')
    self._defaults['default_arrow_lw'] = 1.0
    self._types['default_arrow_lw'] = float
    self._descriptions['default_arrow_opt'] = self.tr('Arrow [Default options]')
    self._defaults['default_arrow_opt'] = '->'
    self._types['default_arrow_opt'] = str

    # Shortcuts
    self._descriptions['shortcut_autoSaveSettings'] = self.tr(
      'Shortcut [Auto save settings]'
    )
    self._defaults['shortcut_autoSaveSettings'] = ''
    self._types['shortcut_autoSaveSettings'] = str
    self._descriptions['shortcut_editSettings'] = self.tr('Shortcut [Edit settings]')
    self._defaults['shortcut_editSettings'] = 'Meta+E'
    self._types['shortcut_editSettings'] = str
    self._descriptions['shortcut_saveSettings'] = self.tr('Shortcut [Save settings]')
    self._defaults['shortcut_saveSettings'] = 'Meta+S'
    self._types['shortcut_saveSettings'] = str
    self._descriptions['shortcut_reload'] = self.tr('Shortcut [Reload]')
    self._defaults['shortcut_reload'] = 'F6'
    self._types['shortcut_reload'] = str
    self._descriptions['shortcut_preview'] = self.tr('Shortcut [Preview]')
    self._defaults['shortcut_preview'] = 'F5'
    self._types['shortcut_preview'] = str
    self._descriptions['shortcut_edit'] = self.tr('Shortcut [Edit...]')
    self._defaults['shortcut_edit'] = 'Ctrl+E'
    self._types['shortcut_edit'] = str
    self._descriptions['shortcut_editDoc'] = self.tr('Shortcut [Edit document]')
    self._defaults['shortcut_editDoc'] = 'Ctrl+Shift+E'
    self._types['shortcut_editDoc'] = str
    self._descriptions['shortcut_group'] = self.tr('Shortcut [Group]')
    self._defaults['shortcut_group'] = 'Ctrl+G'
    self._types['shortcut_group'] = str
    self._descriptions['shortcut_ungroup'] = self.tr('Shortcut [Ungroup]')
    self._defaults['shortcut_ungroup'] = 'Ctrl+Shift+G'
    self._types['shortcut_ungroup'] = str
    self._descriptions['shortcut_newFrame'] = self.tr('Shortcut [New frame]')
    self._defaults['shortcut_newFrame'] = 'Ctrl+F'
    self._types['shortcut_newFrame'] = str
    self._descriptions['shortcut_newFrameTemplate'] = self.tr(
      'Shortcut [Template + number]'
    )
    self._defaults['shortcut_newFrameTemplate'] = 'Ctrl'
    self._types['shortcut_newFrameTemplate'] = str
    self._descriptions['shortcut_saveTemplate'] = self.tr('Shortcut [Save template]')
    self._defaults['shortcut_saveTemplate'] = 'Ctrl+0'
    self._types['shortcut_saveTemplate'] = str
    self._descriptions['shortcut_deleteTemplate'] = self.tr(
      'Shortcut [Delete template]'
    )
    self._defaults['shortcut_deleteTemplate'] = 'Ctrl+-'
    self._types['shortcut_deleteTemplate'] = str
    self._descriptions['shortcut_newText'] = self.tr('Shortcut [New text]')
    self._defaults['shortcut_newText'] = 'Ctrl+T'
    self._types['shortcut_newText'] = str
    self._descriptions['shortcut_newImage'] = self.tr('Shortcut [New image]')
    self._defaults['shortcut_newImage'] = 'Ctrl+I'
    self._types['shortcut_newImage'] = str
    self._descriptions['shortcut_newTikzPicture'] = self.tr(
      'Shortcut [New Tikz picture]'
    )
    self._defaults['shortcut_newTikzPicture'] = 'Ctrl+P'
    self._types['shortcut_newTikzPicture'] = str
    self._descriptions['shortcut_newArrow'] = self.tr('Shortcut [New arrow]')
    self._defaults['shortcut_newArrow'] = 'Ctrl+R'
    self._types['shortcut_newArrow'] = str
    self._descriptions['shortcut_moveUp'] = self.tr('Shortcut [Move up]')
    self._defaults['shortcut_moveUp'] = 'Ctrl+Up'
    self._types['shortcut_moveUp'] = str
    self._descriptions['shortcut_moveDown'] = self.tr('Shortcut [Move down]')
    self._defaults['shortcut_moveDown'] = 'Ctrl+Down'
    self._types['shortcut_moveDown'] = str
    self._descriptions['shortcut_moveTop'] = self.tr('Shortcut [Move top]')
    self._defaults['shortcut_moveTop'] = 'Ctrl+PgUp'
    self._types['shortcut_moveTop'] = str
    self._descriptions['shortcut_moveBottom'] = self.tr('Shortcut [Move bottom]')
    self._defaults['shortcut_moveBottom'] = 'Ctrl+PgDown'
    self._types['shortcut_moveBottom'] = str
    self._descriptions['shortcut_activateGrid'] = self.tr('Shortcut [Grid]')
    self._defaults['shortcut_activateGrid'] = 'Meta+G'
    self._types['shortcut_activateGrid'] = str
    self._descriptions['shortcut_activateObjGuides'] = self.tr(
      'Shortcut [Object guides]'
    )
    self._defaults['shortcut_activateObjGuides'] = 'Meta+Shift+G'
    self._types['shortcut_activateObjGuides'] = str
    self._descriptions['shortcut_showHiddenObjects'] = self.tr(
      'Shortcut [Hidden objects]'
    )
    self._defaults['shortcut_showHiddenObjects'] = 'Meta+H'
    self._types['shortcut_showHiddenObjects'] = str
    self._descriptions['shortcut_hideMenu'] = self.tr('Shortcut [Show/Hide menu]')
    self._defaults['shortcut_hideMenu'] = 'Ctrl+M'
    self._types['shortcut_hideMenu'] = str

    # Colors and line styles
    self._descriptions['color_background'] = self.tr('Color [Background]')
    self._defaults['color_background'] = QtGui.QColor(255, 255, 255)
    self._types['color_background'] = QtGui.QColor
    self._descriptions['color_new_element'] = self.tr('Color [New element]')
    self._defaults['color_new_element'] = QtGui.QColor(220, 220, 220)
    self._types['color_new_element'] = QtGui.QColor
    self._descriptions['pen_element'] = self.tr('Style [Element]')
    self._defaults['pen_element'] = QtGui.QPen(QtGui.QColor(0, 200, 150), 2.0)
    self._types['pen_element'] = QtGui.QPen
    self._descriptions['pen_selected_element'] = self.tr('Style [Selected element]')
    self._defaults['pen_selected_element'] = QtGui.QPen(QtGui.QColor(0, 200, 150), 5.0)
    self._types['pen_selected_element'] = QtGui.QPen
    self._descriptions['pen_group'] = self.tr('Style [Group]')
    self._defaults['pen_group'] = QtGui.QPen(QtGui.QColor(150, 255, 100), 2.0)
    self._types['pen_group'] = QtGui.QPen
    self._descriptions['pen_selected_group'] = self.tr('Style [Selected group]')
    self._defaults['pen_selected_group'] = QtGui.QPen(QtGui.QColor(150, 255, 100), 5.0)
    self._types['pen_selected_group'] = QtGui.QPen
    self._descriptions['pen_hidden_object'] = self.tr('Style [Hidden object]')
    self._defaults['pen_hidden_object'] = QtGui.QPen(QtGui.QColor(100, 150, 200), 2.0)
    self._types['pen_hidden_object'] = QtGui.QPen
    self._descriptions['pen_selected_hidden_object'] = self.tr(
      'Style [Selected hidden object]'
    )
    self._defaults['pen_selected_hidden_object'] = QtGui.QPen(
      QtGui.QColor(100, 150, 200), 5.0
    )
    self._types['pen_selected_hidden_object'] = QtGui.QPen
    self._descriptions['pen_grid1'] = self.tr('Style [grid level 1]')
    self._defaults['pen_grid1'] = QtGui.QPen(QtGui.QColor(0, 0, 0), 0.8)
    self._types['pen_grid1'] = QtGui.QPen
    self._descriptions['pen_grid2'] = self.tr('Style [grid level 2]')
    self._defaults['pen_grid2'] = QtGui.QPen(QtGui.QColor(70, 70, 70), 0.65)
    self._types['pen_grid2'] = QtGui.QPen
    self._descriptions['pen_grid3'] = self.tr('Style [grid level 3]')
    self._defaults['pen_grid3'] = QtGui.QPen(QtGui.QColor(140, 140, 140), 0.5)
    self._types['pen_grid3'] = QtGui.QPen
    self._descriptions['pen_grid4'] = self.tr('Style [grid level 4]')
    self._defaults['pen_grid4'] = QtGui.QPen(QtGui.QColor(190, 190, 190), 0.35)
    self._types['pen_grid4'] = QtGui.QPen
    self._descriptions['pen_object_guide'] = self.tr('Style [object_guide]')
    self._defaults['pen_object_guide'] = QtGui.QPen(QtGui.QColor(180, 140, 50), 1.0)
    self._types['pen_object_guide'] = QtGui.QPen
    self._descriptions['pen_selected_object_guide'] = self.tr(
      'Style [Selected object guide]'
    )
    self._defaults['pen_selected_object_guide'] = QtGui.QPen(
      QtGui.QColor(255, 150, 0), 2.0
    )
    self._types['pen_selected_object_guide'] = QtGui.QPen
    self._descriptions['pen_aligned_object_guide'] = self.tr(
      'Style [Aligned object guide]'
    )
    self._defaults['pen_aligned_object_guide'] = QtGui.QPen(
      QtGui.QColor(255, 0, 0), 2.0
    )
    self._types['pen_aligned_object_guide'] = QtGui.QPen
    self._descriptions['pen_mouse_selection'] = self.tr('Style [Mouse selection]')
    self._defaults['pen_mouse_selection'] = QtGui.QPen(QtGui.QColor(0, 0, 0), 0.75)
    self._types['pen_mouse_selection'] = QtGui.QPen

    self._descriptions['default_paper_w'] = self.tr('Default paper width')
    self._defaults['default_paper_w'] = 364.19536
    self._types['default_paper_w'] = float
    self._descriptions['default_paper_h'] = self.tr('Default paper height')
    self._defaults['default_paper_h'] = 273.14662
    self._types['default_paper_h'] = float
    self._descriptions['refresh_interval'] = self.tr('Display refresh interval')
    self._defaults['refresh_interval'] = 0.03
    self._types['refresh_interval'] = float
    self._descriptions['resize_area_width'] = self.tr('Resizing area width')
    self._defaults['resize_area_width'] = 0.005
    self._types['resize_area_width'] = float
    self._descriptions['magnet_area_width'] = self.tr('Magnetic area width')
    self._defaults['magnet_area_width'] = 0.01
    self._types['magnet_area_width'] = float
    self._descriptions['rotate_prec_deg'] = self.tr('Rotate precision (degrees)')
    self._defaults['rotate_prec_deg'] = 1.0
    self._types['rotate_prec_deg'] = float
    self._descriptions['mouse_crop_prec'] = self.tr('Mouse crop precision')
    self._defaults['mouse_crop_prec'] = 0.01
    self._types['mouse_crop_prec'] = float

    # Hidden settings (can be modified outside properties editor)
    self._defaults['auto_save_settings'] = True
    self._types['auto_save_settings'] = bool
    self._defaults['activate_grid'] = True
    self._types['activate_grid'] = bool
    self._defaults['activate_object_guides'] = True
    self._types['activate_object_guides'] = bool
    self._defaults['show_hidden_objects'] = False
    self._types['show_hidden_objects'] = bool

    self._defaults['templates'] = [
      self.tr('Text frame'),
      '\\begin{frame}{Frame title}\n\\txt{0.0625,0.125,0.875}{\\begin{itemize}\n'
      '\\item First item\n\\begin{itemize}\n\\item First sub-item\n\\vfill\n'
      '\\item Second sub-item\n\\vfill\n\\end{itemize}\n\\item Second item\n'
      '\\end{itemize}}\n\\end{frame}',
      self.tr('Background text frame'),
      '\\begin{frame}{Frame title}\n\\begin{itemize}\n\\item First item\n'
      '\\begin{itemize}\n\\item First sub-item\n\\vfill\n\\item Second sub-item\n'
      '\\vfill\n\\end{itemize}\n\\item Second item\n\\end{itemize}\n\\end{frame}',
      self.tr('Title frame'),
      '\\begin{frame}[plain]\n\\titlepage\n\\end{frame}',
      self.tr('Outline frame'),
      '\\begin{frame}{Outline}\n\\tableofcontents\n\\end{frame}',
    ]
    self._types['templates'] = list

    self._defaults['menuVisible'] = True
    self._types['menuVisible'] = bool
    self._defaults['pagebarVisible'] = True
    self._types['pagebarVisible'] = bool
    self._defaults['window_width'] = 900
    self._types['window_width'] = int
    self._defaults['window_height'] = 750
    self._types['window_height'] = int
    self._defaults['editor_text_width'] = 750
    self._types['editor_text_width'] = int
    self._defaults['editor_text_height'] = 550
    self._types['editor_text_height'] = int
    self._defaults['editor_image_width'] = 400
    self._types['editor_image_width'] = int
    self._defaults['editor_image_height'] = 750
    self._types['editor_image_height'] = int
    self._defaults['editor_tikzpicture_width'] = 750
    self._types['editor_tikzpicture_width'] = int
    self._defaults['editor_tikzpicture_height'] = 600
    self._types['editor_tikzpicture_height'] = int
    self._defaults['editor_arrow_width'] = 400
    self._types['editor_arrow_width'] = int
    self._defaults['editor_arrow_height'] = 450
    self._types['editor_arrow_height'] = int
    self._defaults['editor_group_width'] = 400
    self._types['editor_group_width'] = int
    self._defaults['editor_group_height'] = 500
    self._types['editor_group_height'] = int
    self._defaults['editor_frame_width'] = 750
    self._types['editor_frame_width'] = int
    self._defaults['editor_frame_height'] = 750
    self._types['editor_frame_height'] = int
    self._defaults['editor_document_width'] = 750
    self._types['editor_document_width'] = int
    self._defaults['editor_document_height'] = 750
    self._types['editor_document_height'] = int
    self._defaults['editor_settings_width'] = 750
    self._types['editor_settings_width'] = int
    self._defaults['editor_settings_height'] = 750
    self._types['editor_settings_height'] = int


settings = Settings()
settings.load('bed', 'bed')

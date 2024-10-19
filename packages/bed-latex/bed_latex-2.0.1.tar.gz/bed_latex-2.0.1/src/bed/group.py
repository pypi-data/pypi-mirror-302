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

# This file defines the Group class (group of elements, see element.py)

import math

from .editor import (
  BedCheckBox,
  BedDoubleSpinBox,
  BedLineEdit,
  BedPushButton,
  PropertiesEditor,
)
from .element import Element
from .settings import settings


class Group(Element):
  """Defines a group of Elements (see element.py)"""

  def __init__(self, *args, **kwargs):
    """Initialisation"""
    super().__init__()
    self.init(*args, **kwargs)
    self.refresh_xguides()
    self.refresh_yguides()

  def init(
    self,
    x=0,
    y=0,
    w=1,
    h=1,
    minw=settings.epsilon,
    minh=settings.epsilon,
    angle_deg=0,
    pagesList=(),
    hover=0,
    selected=False,
    xguides_names=('left', 'center', 'right'),
    yguides_names=('bottom', 'center', 'top'),
    paper_ratio=1,
    current_align_x=(),
    current_align_y=(),
    locked_props=None,
    origratio=None,
    elements=(),
  ):
    """Initialisation from parameters (deep copy of parameters)"""
    super().init(
      x,
      y,
      w,
      h,
      minw,
      minh,
      angle_deg,
      '',
      pagesList,
      None,
      hover,
      selected,
      None,
      '',
      xguides_names,
      yguides_names,
      paper_ratio,
      current_align_x,
      current_align_y,
      locked_props,
    )
    # default widht / height ratio
    if origratio:
      self.origratio = origratio
    else:
      self.origratio = w / h
    # Check if the width/height ratio is locked to the default value
    if locked_props is None and self.isOrigratio():
      self.locked_props = ['ratio']
    self.elements = []
    # elements
    for el in elements:
      self.elements.append(el.copy())
      self.elements[-1].group = self

  def copy(self, copy_elements=True):
    """Deep copy of the group"""
    elems = self.elements if copy_elements else []
    return Group(
      self.x,
      self.y,
      self.w,
      self.h,
      self.minw,
      self.minh,
      self.angle_deg,
      self.pagesList,
      self.hover,
      self.selected,
      self.xguides_names,
      self.yguides_names,
      self.paper_ratio,
      self.current_align_x,
      self.current_align_y,
      self.locked_props,
      self.origratio,
      elems,
    )

  def isOrigratio(self):
    """Check if the ratio preserves the original ratio"""
    return abs(self.w - self.h * self.origratio) < settings.epsilon

  def delete(self):
    """Remove all references to the group in contained elements"""
    for el in self.elements:
      el.group = None

  def addElement(self, element, compute_geometry=True, append=True):
    """Add an element to the group"""
    element.group = self
    # Check if it is the first one
    if self.elements:
      # Update elements list and group borders
      l = min(self.get_xguide('left'), element.get_xguide('left'))
      r = max(self.get_xguide('right'), element.get_xguide('right'))
      t = min(self.get_yguide('top'), element.get_yguide('top'))
      b = max(self.get_yguide('bottom'), element.get_yguide('bottom'))
    else:
      # Init group
      l = element.get_xguide('left')
      r = element.get_xguide('right')
      t = element.get_yguide('top')
      b = element.get_yguide('bottom')
    # Append or add to the top of the list
    if append:
      self.elements.append(element)
    else:
      self.elements.insert(0, element)
    # Update pagesList
    for page in element.pagesList:
      if page not in self.pagesList:
        self.pagesList.append(page)
    # Update the group position/size/angle
    if compute_geometry:
      self.angle_deg = 0
      self.angle_rad = 0
      self.x = l
      self.y = t
      self.w = r - l
      self.h = b - t
      self.origratio = self.w / self.h
      self.refresh_xguides()
      self.refresh_yguides()

  def draw(self, framepage, painter):
    """Drawing function (called by the painter, see painter.py)"""
    # use the super function (see element.py) with isgroup=True
    super().draw(framepage, painter, isgroup=True)

  def saveGeometry(self):
    """Initialisation before a move/resize/rotate event"""
    # Just remember the initial geometry + geometry of elements
    super().saveGeometry()
    for el in self.elements:
      el.saveGeometry()

  def change_geom(self, Dx, Dy, dx, dy, extern_xguides, extern_yguides):
    """Change the geometry of the group according to mouse move.
    Decide wether to move/resize/rotate depending on mouse position and key modifiers.
    """
    # Use super function (see element.py)
    super().change_geom(Dx, Dy, dx, dy, extern_xguides, extern_yguides)
    # Apply the changes to all the contained elements
    self.apply_change_to_elements()

  def apply_change_to_elements(self):
    """Apply any change in the Group geometry to all the contained elements"""
    # init resize
    alphaw = self.w / self.w0
    alphah = self.h / self.h0
    # init rotate
    for el in self.elements:
      # Move x,y
      # Relative initial position of element in group
      relx0 = el.x0 - self.x0
      rely0 = el.y0 - self.y0
      # Relative inital position in rotated frame of group
      rotrelx0 = (
        relx0 * math.cos(self.angle_rad0)
        - rely0 * math.sin(self.angle_rad0) / self.paper_ratio
      )
      rotrely0 = relx0 * math.sin(
        self.angle_rad0
      ) * self.paper_ratio + rely0 * math.cos(self.angle_rad0)
      # Resizing
      rotrelx = rotrelx0 * alphaw
      rotrely = rotrely0 * alphah
      # Rotation
      relx = (
        rotrelx * math.cos(self.angle_rad)
        + rotrely * math.sin(self.angle_rad) / self.paper_ratio
      )
      rely = -rotrelx * math.sin(
        self.angle_rad
      ) * self.paper_ratio + rotrely * math.cos(self.angle_rad)
      # Move
      el.x = self.x + relx
      el.y = self.y + rely
      # Resize w,h
      # Initial angle between element and group
      dangle0 = el.angle_rad0 - self.angle_rad0
      # Compute new angle
      dangle = math.atan2(math.sin(dangle0) * alphah, math.cos(dangle0) * alphaw)
      # Initial position of opposite corner (D)
      rxD0 = el.w0 * math.cos(dangle0) + el.h0 * math.sin(dangle0) / self.paper_ratio
      ryD0 = -el.w0 * math.sin(dangle0) * self.paper_ratio + el.h0 * math.cos(dangle0)
      # New position
      rxD = rxD0 * alphaw
      ryD = ryD0 * alphah
      # New position in the element frame
      el.w = max(
        el.minw, rxD * math.cos(dangle) - ryD * math.sin(dangle) / self.paper_ratio
      )
      el.h = max(
        el.minh, rxD * math.sin(dangle) * self.paper_ratio + ryD * math.cos(dangle)
      )
      if 'ratio' in el.locked_props:
        if el.h0 / el.w0 * el.w > el.minh and (
          el.h * el.w0 > el.w * el.h0 or el.w0 / el.h0 * el.h < el.minw
        ):
          el.h = el.h0 / el.w0 * el.w
        else:
          el.w = el.w0 / el.h0 * el.h
      if 'w' in el.locked_props or el.w0 == el.minw:
        el.w = el.w0
      if 'h' in el.locked_props or el.h0 == el.minh:
        el.h = el.h0
      # Rotate angle
      el.angle_rad = self.angle_rad + dangle
      el.angle_deg = el.angle_rad * 180 / math.pi
      # Refresh guides
      el.refresh_xguides()
      el.refresh_yguides()
      if type(el) is Group:
        el.apply_change_to_elements()

  def edit(self, parentwindow):
    """Launch the PropertiesEditor (see editor.py) to edit the Group properties."""
    # Save geometry of the group
    self.saveGeometry()
    # Compute the pagesCMD of the group from the values in elements
    pagesCMD = self.elements[0].pagesCMD
    for el in self.elements[1:]:
      if el.pagesCMD != pagesCMD:
        pagesCMD = None
        break

    # Initial values of props (before editing)
    init_values = [
      self.x,
      self.y,
      self.w,
      self.h,
      ('ratio' in self.locked_props),
      None,
      self.angle_deg,
      pagesCMD,
      ','.join(self.xguides_names),
      ','.join(self.yguides_names),
    ]

    # Define all the onChange functions (see editor.py)
    def oCw(parent):
      """Width -> update height if needed"""
      parent.changing = True
      if parent.bedwidgets[4].value():
        prev_w = parent.bedwidgets[2].prev_value
        prev_h = parent.bedwidgets[3].value()
        w = parent.bedwidgets[2].value()
        h = w * prev_h / prev_w
        if h < self.minh:
          h = self.minh
          w = h * prev_w / prev_h
          parent.bedwidgets[2].setValue(w)
        parent.bedwidgets[3].setValue(h)
      parent.changing = False

    def oCh(parent):
      """Height -> update width if needed"""
      parent.changing = True
      if parent.bedwidgets[4].value():
        prev_w = parent.bedwidgets[2].value()
        prev_h = parent.bedwidgets[3].prev_value
        h = parent.bedwidgets[3].value()
        w = h * prev_w / prev_h
        if w < self.minw:
          w = self.minw
          h = w * prev_h / prev_w
          parent.bedwidgets[3].setValue(h)
        parent.bedwidgets[2].setValue(w)
      parent.changing = False

    def oCreset(parent):
      """Reset to orig. ratio button -> update height"""
      parent.changing = True
      w = parent.bedwidgets[2].value()
      h = w / self.origratio
      parent.bedwidgets[3].setValue(h)
      parent.changing = False

    # Define BedWidget for each prop (see editor.py)
    bwx = BedDoubleSpinBox(init_values[0], -1, 2, 0.01, 4, label='x')
    bwy = BedDoubleSpinBox(init_values[1], -1, 2, 0.01, 4, label='y')
    bww = BedDoubleSpinBox(
      init_values[2], self.minw, 2, 0.01, 4, label='w', onChange=oCw
    )
    bwh = BedDoubleSpinBox(
      init_values[3], self.minh, 2, 0.01, 4, label='h', onChange=oCh
    )
    bwlock = BedCheckBox(init_values[4], label=' ', checklabel=self.tr('Lock ratio'))
    bwreset = BedPushButton(
      label=' ', buttonlabel=self.tr('Original ratio'), onChange=oCreset
    )
    bwangle = BedDoubleSpinBox(init_values[6], -180, 360, 5, 2, label=self.tr('Angle'))
    bwpages = BedLineEdit(init_values[7], label=self.tr('Pages'))
    bwxguides = BedLineEdit(init_values[8], label=self.tr('x guides'))
    bwyguides = BedLineEdit(init_values[9], label=self.tr('y guides'))
    bedwidgets = [
      bwx,
      bwy,
      bww,
      bwh,
      bwlock,
      bwreset,
      bwangle,
      bwpages,
      bwxguides,
      bwyguides,
    ]
    values = PropertiesEditor.getValues(
      parentwindow, bedwidgets, settings, 'group', self.tr('Group')
    )

    # Check if values have changed
    if values:
      # Update properties
      self.x = values[0]
      self.y = values[1]
      self.w = values[2]
      self.h = values[3]
      if values[4]:
        if 'ratio' not in self.locked_props:
          self.locked_props.append('ratio')
      elif 'ratio' in self.locked_props:
        self.locked_props.remove('ratio')
      self.angle_deg = values[6]
      self.angle_rad = values[6] * math.pi / 180
      if values[7]:
        for el in self.elements:
          el.pagesCMD = values[7]
      self.xguides_names = values[8].split(',')
      self.yguides_names = values[9].split(',')
      self.refresh_xguides()
      self.refresh_yguides()
      # Apply the change in geometry to all the contained elements
      self.apply_change_to_elements()
      return True
    return False

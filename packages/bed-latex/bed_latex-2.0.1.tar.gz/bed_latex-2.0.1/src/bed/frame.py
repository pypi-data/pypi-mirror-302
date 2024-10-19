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

# This file defines the Frame class (Beamer frame)

import xml.etree.ElementTree as ET

from PySide6 import QtCore

from .editor import BedAdjustTextEdit, PropertiesEditor
from .element import Arrow, Image, Text, TikzPicture
from .group import Group
from .helpers import spacelines, striplines
from .settings import settings


class Frame(QtCore.QObject):
  """Frame class represents a complete Beamer frame.
  Contains a title and elements (texts, images, arrows)
  """

  def __init__(self, *args, **kwargs):
    """Initialisation"""
    super().__init__()
    if len(args) > 0 and type(args[0]) is ET.Element:
      self.readxml(*args, **kwargs)
    else:
      self.init(*args, **kwargs)

  def init(
    self,
    title='',
    elements=(),
    groups=(),
    pageimgs=(None,),
    firstpage=0,
    npages=1,
    before='',
  ):
    """Initialisation from parameters.
    This function is used for the copy of a frame,
    so the init of properties is done with a deep copy.
    """
    self.title = title
    # Elements (text/image/arrow)
    self.elements = []
    # Groups of elements (see group.py)
    self.groups = []
    # Deep copy of groups/elements
    dic = {}
    for g in groups:
      ng = g.copy(copy_elements=False)
      self.groups.append(ng)
      dic[g] = ng
    for el in elements:
      self.elements.append(el.copy())
      if el.group:
        ng = dic[el.group]
        ng.addElement(self.elements[-1], compute_geometry=False)
    # First page the frame appears in the document
    self.firstpage = firstpage
    self.npages = npages
    self.pageimgs = list(pageimgs)
    # Latex commands that appear just before the frame
    self.before = before

  def readxml(self, xmlFrame, pageimgs, paper_ratio, paper_h):
    """Initialisation from xml file"""
    # Same as init() but reads the values from the xml tree instead of function args.
    self.title = striplines(xmlFrame.get('title').strip(), 4)
    self.firstpage = int(xmlFrame.get('first_page')) - 1
    self.npages = int(xmlFrame.get('n_pages'))
    self.pageimgs = pageimgs[self.firstpage : self.firstpage + self.npages]
    self.before = striplines(xmlFrame.get('before').strip(), 2)
    self.groups = []
    for _ in range(int(xmlFrame.get('n_groups'))):
      self.groups.append(Group(paper_ratio=paper_ratio))
    self.elements = []
    for xml_element in reversed(xmlFrame):
      if xml_element.tag == 'img':
        self.elements.insert(
          0, Image(xml_element, self.npages, self.pageimgs, paper_ratio)
        )
      elif xml_element.tag == 'tkp':
        self.elements.insert(
          0, TikzPicture(xml_element, self.npages, self.pageimgs, paper_ratio)
        )
      elif xml_element.tag == 'txt':
        self.elements.insert(
          0, Text(xml_element, self.npages, self.pageimgs, paper_ratio)
        )
      elif xml_element.tag == 'arw':
        self.elements.insert(
          0, Arrow(xml_element, self.npages, self.pageimgs, paper_ratio, paper_h)
        )
      if self.elements[0].group < 0:
        self.elements[0].group = None
      else:
        self.groups[self.elements[0].group].addElement(self.elements[0], append=False)

  def copy(self):
    """Deep copy except for pageimgs (pdf preview)"""
    return Frame(
      self.title,
      self.elements,
      self.groups,
      self.pageimgs,
      self.firstpage,
      self.npages,
      self.before,
    )

  def writeTeX(self):
    """Write the TeX extract corresponding to the frame properties"""
    # Try to get correct indenting
    tex = ''
    if self.before.strip():
      tex += spacelines(self.before.strip(), 2) + '\n'
    tex += '  \\begin{frame}'
    first = True
    for line in self.title.split('\n'):
      if first:
        first = False
      else:
        tex += '    '
      tex += line + '\n'
    for el in self.elements:
      tex += el.writeTeX(self.groups) + '\n'
    tex += '  \\end{frame}'
    return tex

  def group(self, paper_ratio):
    """Group selected elements in the frame"""
    g = Group(paper_ratio=paper_ratio)
    tmpg = []
    # Look if groups are selected
    # reverse list to be able to delete groups without perturbing loop
    for gr in reversed(self.groups):
      if gr.selected:
        # Add all elements of the selected group
        tmpg += gr.elements
        # Delete the old group
        self.groups.remove(gr)
    # Look for selected elements
    for el in self.elements:
      if el.selected or el in tmpg:
        # unselect and deactivate hover properties (see refreshHovering)
        el.selected = False
        el.hover = 0
        # Add
        g.addElement(el)
    # If the group is not empty
    if g.elements:
      # Select it
      g.selected = True
      # add it to the frame group list
      self.groups.append(g)

  def ungroup(self):
    """Ungroup selected groups"""
    # Look if groups are selected
    # reverse list to be able to delete groups without perturbing loop
    for g in reversed(self.groups):
      if g.selected:
        # Free all contained elements
        for el in g.elements:
          el.selected = True
          el.group = None
        # delete group from the frame list
        self.groups.remove(g)

  def tmpgroup(self, paper_ratio):
    """Group selected elements/groups in the frame in a temporary group
    Useful for moving multiple elements without creating a permanent group
    see painter.py
    """
    g = Group(paper_ratio=paper_ratio)
    # Look for selected elements/groups
    for gel in self.elements + self.groups:
      if gel.selected:
        # unselect and deactivate hover properties (see refreshHovering)
        gel.selected = False
        gel.hover = 0
        # Add
        g.addElement(gel)
    # If the group is not empty
    if g.elements:
      # Select it
      g.selected = True
      # add it to the frame group list
      self.groups.append(g)

  def untmpgroup(self):
    """Ungroup the temporary group only"""
    # Look if groups are selected
    # reverse list to be able to delete groups without perturbing loop
    # But stop after the first removal
    # (to avoid deleting groups contained in the tmpgroup)
    for g in reversed(self.groups):
      if g.selected:
        # Free all contained elements
        for el in g.elements:
          el.selected = True
          el.group = None
        # delete group from the frame list
        self.groups.remove(g)
        break

  def xGuides(self, framepage):
    """Compute the object guides of the frame along x"""
    # Look for all groups and elements positions to get guides when
    # moving an object in the frame (allow to easily align elements/groups)
    xg = []
    # Only do it if Object guides are activated
    if settings.activate_object_guides:
      # Browse the elements/groups lists
      for gel in self.elements + self.groups:
        # Don't consider selected objects (they will not guide themselves)
        # Also elements in selected groups should not be considered
        if (
          gel.selected
          or (gel.group and gel.group.selected)
          or not (settings.show_hidden_objects or gel.isvisible(framepage))
        ):
          continue
        # Add object guides to the list
        xg += gel.xguides
    # If the grid is activated
    # Add grid guides to the list
    if settings.activate_grid:
      for k in range(settings.Ngrid + 1):
        xg.append(k / settings.Ngrid)
    return xg

  def yGuides(self, framepage):
    """Compute the object guides of the frame along x"""
    # See comments of xGuides
    yg = []
    if settings.activate_object_guides:
      for gel in self.elements + self.groups:
        if (
          gel.selected
          or (gel.group and gel.group.selected)
          or not (settings.show_hidden_objects or gel.isvisible(framepage))
        ):
          continue
        # Add object guides to the list
        yg += gel.yguides
    if settings.activate_grid:
      for k in range(settings.Ngrid + 1):
        yg.append(k / settings.Ngrid)
    return yg

  def draw(self, framepage, painter):
    """Draw the current state of the frame page"""
    # Destination rectangle for the background image
    rect = QtCore.QRect(0, 0, painter.parent.width(), painter.parent.height())
    if self.pageimgs[framepage]:
      painter.drawImage(rect, self.pageimgs[framepage])
    else:
      painter.setBrush(settings.color_background)
      painter.drawRect(rect)
      painter.setBrush(QtCore.Qt.NoBrush)
    # Draw borders
    painter.setPen(settings.pen_grid1)
    painter.drawVline(0)
    painter.drawVline(1)
    painter.drawHline(0)
    painter.drawHline(1)
    # Draw guides
    # Check if there is any selected objects
    if any(gel.selected for gel in self.groups + self.elements):
      # Fixed grid
      if settings.activate_grid:
        for k in range(1, settings.Ngrid):
          if int(4 * k / settings.Ngrid) == 4 * k / settings.Ngrid:
            painter.setPen(settings.pen_grid1)
          elif int(8 * k / settings.Ngrid) == 8 * k / settings.Ngrid:
            painter.setPen(settings.pen_grid2)
          elif int(16 * k / settings.Ngrid) == 16 * k / settings.Ngrid:
            painter.setPen(settings.pen_grid3)
          else:
            painter.setPen(settings.pen_grid4)
          painter.drawVline(k / settings.Ngrid)
          painter.drawHline(k / settings.Ngrid)
      # Object guides
      frame_xguides = self.xGuides(framepage)
      frame_yguides = self.yGuides(framepage)
      if settings.activate_object_guides or settings.activate_grid:
        # Unselected objects guides in background
        painter.setPen(settings.pen_object_guide)
        for gel in self.groups + self.elements:
          if (
            settings.activate_object_guides
            and not gel.group
            and not gel.selected
            and (settings.show_hidden_objects or gel.isvisible(framepage))
          ):
            for xg in gel.xguides:
              painter.drawVline(xg)
            for yg in gel.yguides:
              painter.drawHline(yg)
        # Selected objects guides in foreground
        for gel in self.groups + self.elements:
          if gel.selected and not gel.group:
            gel.refresh_align_guides(frame_xguides, frame_yguides)
            for ng, xg in zip(gel.xguides_names, gel.xguides):
              if ng in gel.current_align_x:
                painter.setPen(settings.pen_aligned_object_guide)
              else:
                painter.setPen(settings.pen_selected_object_guide)
              painter.drawVline(xg)
            for ng, yg in zip(gel.yguides_names, gel.yguides):
              if ng in gel.current_align_y:
                painter.setPen(settings.pen_aligned_object_guide)
              else:
                painter.setPen(settings.pen_selected_object_guide)
              painter.drawHline(yg)
    # Draw elements / groups
    groupscount = [len(grp.elements) for grp in self.groups]
    # Loop over elements
    for el in self.elements:
      if el.isvisible(framepage):
        el.draw(framepage, painter)
        # The groups are drawn at the same time as their uppermost element
        if el.group:
          kgrp = self.groups.index(el.group)
          groupscount[kgrp] -= 1
          if groupscount[kgrp] == 0:
            el.group.draw(framepage, painter)
    # In case we did not draw some group
    # (in particular for the temporary group (tmpgroup))
    for kgrp, grp in enumerate(self.groups):
      if groupscount[kgrp] > 0 and grp.isvisible(framepage):
        grp.draw(framepage, painter)

  def edit(self, parentwindow):
    """Launch the PropertiesEditor (see editor.py) to edit the Frame properties."""
    # Initial values of props (before editing)
    init_values = [self.before, self.title]
    # Define BedWidget for each prop (see editor.py)
    bwbefore = BedAdjustTextEdit(
      init_values[0], label=self.tr('Before frame'), highlight=True
    )
    bwtitle = BedAdjustTextEdit(
      init_values[1], label=self.tr('Title & header'), highlight=True
    )
    bedwidgets = [bwbefore, bwtitle]
    values = PropertiesEditor.getValues(
      parentwindow, bedwidgets, settings, 'frame', self.tr('Frame')
    )

    # Check if values have changed
    if values:
      # Update properties
      self.before = values[0]
      self.title = values[1]
      return True
    return False

  def clean_imgs(self):
    """Clean all preview images from the frame and its elements."""
    self.pageimgs = [None] * self.npages
    for el in self.elements:
      el.clean_imgs()

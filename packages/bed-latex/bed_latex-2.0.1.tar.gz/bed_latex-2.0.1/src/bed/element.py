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

# This file defines the Element class,
# and the Text, Image, TikzPicture, and Arrow class that inherit from it.

import math
import os
import re
import xml.etree.ElementTree as ET

from PySide6 import QtCore, QtGui, QtWidgets

from .editor import (
  BedAdjustTextEdit,
  BedCheckBox,
  BedComboBox,
  BedDoubleSpinBox,
  BedLineEdit,
  BedPushButton,
  PropertiesEditor,
)
from .helpers import argmax, argmin, spacelines, striplines
from .settings import settings


class Element(QtCore.QObject):
  """Defines any element that appears in a frame.
  Not to be used directly.
  It just defines common properties of text blocks, images and arrows.
  Each element is a rectangle ABCD whose position/size/orientation is defined by
  x,y (position of A)
  w = AB
  h = AC
  angle = angle between x axis and AB
  """

  def __init__(self, *args, **kwargs):
    """Initialisation"""
    super().__init__()
    # Init position of the mouse
    self.mousex = 0
    self.mousey = 0
    # Init keyboard modifiers
    self.metamod = False
    self.shiftmod = False
    self.altmod = False

  def init(
    self,
    x,
    y,
    w,
    h,
    minw=0,
    minh=0,
    angle_deg=0,
    pagesCMD='',
    pagesList=(),
    imgs=None,
    hover=0,
    selected=False,
    group=None,
    before='',
    xguides_names=(),
    yguides_names=(),
    paper_ratio=1,
    current_align_x=(),
    current_align_y=(),
    locked_props=(),
  ):
    """Initialisation from parameters.
    This function is used for the copy of an element,
    so the init of properties is done with a deep copy.
    """
    # Position
    self.x = x
    self.y = y
    # Size
    self.w = w
    self.h = h
    # Minimum size
    self.minw = minw
    self.minh = minh
    # Orientation
    self.angle_deg = angle_deg
    self.angle_rad = angle_deg * math.pi / 180
    # Command that list the pages where the element appears (ex: 1-2, 3, 9-)
    self.pagesCMD = pagesCMD
    # List of these pages
    self.pagesList = list(pagesList)
    # Images of the element in each page where it appears
    self.imgs = imgs
    # Code describing the position of the mouse over the object
    # to decide wether to move (mouse at the center) or resize (mouse on the edge)...
    self.hover = hover
    # Selection status
    self.selected = selected
    # Group containing the element
    self.group = group
    # Latex commands that appear just before the element
    self.before = before
    # Guides names for this element (A,B,... or AB,AC... or left,bottom,... or center)
    self.xguides_names = list(xguides_names)
    self.yguides_names = list(yguides_names)
    # Paper width/height ratio
    self.paper_ratio = paper_ratio
    # Find the coordinates of the element guides
    self.refresh_xguides()
    self.refresh_yguides()
    # List of aligned guides
    self.current_align_x = list(current_align_x)
    self.current_align_y = list(current_align_y)
    # Locked properties of the object (ratio, width...)
    if locked_props is None:
      self.locked_props = None
    else:
      self.locked_props = list(locked_props)

  def readxml(self, xmlElement, npages, slide_imgs, paper_ratio):
    """Initialisation from xml file"""
    # Same as init() but reads the values from the xml tree instead of function args.
    self.x = float(xmlElement.get('x'))
    self.y = float(xmlElement.get('y'))
    self.w = float(xmlElement.get('w'))
    self.h = float(xmlElement.get('h'))
    self.minw = 0
    self.minh = 0
    self.angle_deg = float(xmlElement.get('angle'))
    self.angle_rad = self.angle_deg * math.pi / 180
    self.pagesCMD = xmlElement.get('pages')
    if self.pagesCMD == '1-':
      self.pagesCMD = ''
    self.hover = 0
    self.selected = False
    self.group = int(xmlElement.get('group')) - 1
    self.before = striplines(xmlElement.get('before').strip(), 4)
    self.read_pagesCMD(npages)
    self.extractImg(slide_imgs)
    self.xguides_names = []
    self.yguides_names = []
    self.paper_ratio = paper_ratio
    self.refresh_xguides()
    self.refresh_yguides()
    self.current_align_x = []
    self.current_align_y = []
    self.locked_props = []

  def read_pagesCMD(self, npages=1):
    """Read the pagesCMD (Beamer overlays) field of the element
    to compute the list of pages in which it is visible.
    npages is the number of pages in the parent frame.
    """

    # If nothing is specified, the element appears in each frame page
    if self.pagesCMD == '':
      self.pagesList = []
      for p in range(npages):
        self.pagesList.append(p)
    else:
      # Split the comma-separated list of intervals
      split = re.split(',', self.pagesCMD)
      pages = set()
      for rg in split:
        # For each interval, get the start/end
        mrg = re.match(r'-(\d+)|(\d+)(?:-(\d*))?', rg)
        if mrg.group(1):
          for p in range(int(mrg.group(1))):
            pages.add(p)
        elif mrg.group(3) is None:
          pages.add(int(mrg.group(2)) - 1)
        else:
          first = int(mrg.group(2))
          last = int(mrg.group(3)) if mrg.group(3) else max(npages, first)
          for p in range(first - 1, last):
            pages.add(p)
      self.pagesList = list(pages)

  def extractImg(self, slide_imgs):
    """Extract rectangle in each pdf page corresponding the element."""
    self.imgs = []
    # Define rotations (+/- angle)
    rot = QtGui.QTransform()
    rot.rotate(self.angle_deg)
    mrot = QtGui.QTransform()
    mrot.rotate(-self.angle_deg)
    # Coordinate of 0,0 of original image in rotated image
    img_w = slide_imgs[0].width()
    img_h = slide_imgs[0].height()
    x0 = min(
      0,
      -img_h * math.sin(self.angle_rad),
      img_w * math.cos(self.angle_rad),
      img_w * math.cos(self.angle_rad) - img_h * math.sin(self.angle_rad),
    )
    y0 = min(
      0,
      img_h * math.cos(self.angle_rad),
      +img_w * math.sin(self.angle_rad),
      +img_w * math.sin(self.angle_rad) + img_h * math.cos(self.angle_rad),
    )
    # Coordinate of element in rotated image
    rx = (
      img_w * self.x * math.cos(self.angle_rad)
      - img_h * self.y * math.sin(self.angle_rad)
      - x0
    )
    ry = (
      img_h * self.y * math.cos(self.angle_rad)
      + img_w * self.x * math.sin(self.angle_rad)
      - y0
    )
    rect = QtCore.QRectF(rx, ry, self.w * img_w, self.h * img_h)
    # Do the rotation and cutting for each slide
    for p, img in enumerate(slide_imgs):
      if p in self.pagesList:
        # rotate
        rimg = img.transformed(rot)
        # cut rectangle around element
        self.imgs.append(rimg.copy(rect.toRect()))
        # erase element in slide image
        qp = QtGui.QPainter(rimg)
        qp.fillRect(rect, settings.color_background)
        qp.end()
        rrimg = rimg.transformed(mrot)
        rorig = QtCore.QRectF(
          (rrimg.width() - img_w) / 2, (rrimg.height() - img_h) / 2, img_w, img_h
        )
        slide_imgs[p] = rrimg.copy(rorig.toRect())
      else:
        self.imgs.append(None)

  def isvisible(self, framepage):
    return settings.show_hidden_objects or self.selected or framepage in self.pagesList

  def draw(self, framepage, painter, isgroup=False, img=None):
    """Drawing function (called by the painter, see painter.py)"""
    # Rotation of coordinates
    painter.rotate(-self.angle_deg)
    # New coordinates of element
    rx = (painter.parent.width() * self.x) * math.cos(self.angle_rad) - (
      painter.parent.height() * self.y
    ) * math.sin(self.angle_rad)
    ry = (painter.parent.height() * self.y) * math.cos(self.angle_rad) + (
      painter.parent.width() * self.x
    ) * math.sin(self.angle_rad)
    rw = self.w * painter.parent.width()
    rh = self.h * painter.parent.height()
    # Where to draw the rectangle in painter
    rect = QtCore.QRectF(rx, ry, rw, rh)
    # Drawing of the element:
    # If visible we draw the element (or color the rect if no preview available)
    if framepage in self.pagesList:
      if img:
        painter.drawImage(rect, img)
      elif self.imgs and framepage < len(self.imgs) and self.imgs[framepage]:
        painter.drawImage(rect, self.imgs[framepage])
      elif not isgroup:
        painter.setBrush(settings.color_new_element)
        # Draw a frame around element
        # Color/width of frame around element depends on visibility, selection...
      if isgroup:
        if self.selected:
          painter.setPen(settings.pen_selected_group)
        else:
          painter.setPen(settings.pen_group)
      elif self.selected:
        painter.setPen(settings.pen_selected_element)
      else:
        painter.setPen(settings.pen_element)
    elif self.selected:
      painter.setPen(settings.pen_selected_hidden_object)
    else:
      painter.setPen(settings.pen_hidden_object)
    painter.drawRect(rect)
    painter.setBrush(QtCore.Qt.NoBrush)
    painter.resetTransform()

  def get_xguide(self, guidetype):
    """Get the x coordinate of an element guide"""
    if guidetype == 'A':
      return self.x
    if guidetype == 'B':
      return self.x + self.w * math.cos(self.angle_rad)
    if guidetype == 'C':
      return self.x + self.h / self.paper_ratio * math.sin(self.angle_rad)
    if guidetype == 'D':
      return (
        self.x
        + self.w * math.cos(self.angle_rad)
        + self.h / self.paper_ratio * math.sin(self.angle_rad)
      )
    if guidetype == 'left':
      return min(
        self.get_xguide('A'),
        self.get_xguide('B'),
        self.get_xguide('C'),
        self.get_xguide('D'),
      )
    if guidetype == 'right':
      return max(
        self.get_xguide('A'),
        self.get_xguide('B'),
        self.get_xguide('C'),
        self.get_xguide('D'),
      )
    if guidetype == 'AB':
      return (self.get_xguide('A') + self.get_xguide('B')) / 2
    if guidetype == 'AC':
      return (self.get_xguide('A') + self.get_xguide('C')) / 2
    if guidetype == 'BD':
      return (self.get_xguide('B') + self.get_xguide('D')) / 2
    if guidetype == 'CD':
      return (self.get_xguide('C') + self.get_xguide('D')) / 2
    if guidetype == 'center':
      return (self.get_xguide('A') + self.get_xguide('D')) / 2

  def get_yguide(self, guidetype):
    """Get the y coordinate of an element guide"""
    if guidetype == 'A':
      return self.y
    if guidetype == 'B':
      return self.y - self.w * self.paper_ratio * math.sin(self.angle_rad)
    if guidetype == 'C':
      return self.y + self.h * math.cos(self.angle_rad)
    if guidetype == 'D':
      return (
        self.y
        - self.w * self.paper_ratio * math.sin(self.angle_rad)
        + self.h * math.cos(self.angle_rad)
      )
    if guidetype == 'top':
      return min(
        self.get_yguide('A'),
        self.get_yguide('B'),
        self.get_yguide('C'),
        self.get_yguide('D'),
      )
    if guidetype == 'bottom':
      return max(
        self.get_yguide('A'),
        self.get_yguide('B'),
        self.get_yguide('C'),
        self.get_yguide('D'),
      )
    if guidetype == 'AB':
      return (self.get_yguide('A') + self.get_yguide('B')) / 2
    if guidetype == 'AC':
      return (self.get_yguide('A') + self.get_yguide('C')) / 2
    if guidetype == 'BD':
      return (self.get_yguide('B') + self.get_yguide('D')) / 2
    if guidetype == 'CD':
      return (self.get_yguide('C') + self.get_yguide('D')) / 2
    if guidetype == 'center':
      return (self.get_yguide('A') + self.get_yguide('D')) / 2

  def refresh_xguides(self):
    """Refresh the coordinates of all x guides"""
    self.xguides = []
    for gname in reversed(self.xguides_names):
      g = self.get_xguide(gname)
      if g is None:
        self.xguides_names.remove(gname)
      else:
        self.xguides.append(g)
    self.xguides.reverse()

  def refresh_yguides(self):
    """Refresh the coordinates of all y guides"""
    self.yguides = []
    for gname in reversed(self.yguides_names):
      g = self.get_yguide(gname)
      if g is None:
        self.yguides_names.remove(gname)
      else:
        self.yguides.append(g)
    self.yguides.reverse()

  def refresh_align_guides(self, extern_xguides, extern_yguides):
    """Recheck which guides are aligned"""
    self.current_align_x = []
    self.current_align_y = []
    for gn, g in zip(self.xguides_names, self.xguides):
      for eg in extern_xguides:
        if abs(eg - g) < settings.epsilon:
          self.current_align_x.append(gn)
    for gn, g in zip(self.yguides_names, self.yguides):
      for eg in extern_yguides:
        if abs(eg - g) < settings.epsilon:
          self.current_align_y.append(gn)

  def refreshHover(self, x, y):
    """Determine if the mouse pointer (x,y coordinates) is over the element
    And if it is in the middle or border of the element (for move or resize actions)
    """
    # Keyboard modifiers status
    self.shiftmod = (
      QtWidgets.QApplication.queryKeyboardModifiers() & QtCore.Qt.ShiftModifier
    )
    self.metamod = (
      QtWidgets.QApplication.queryKeyboardModifiers() & QtCore.Qt.MetaModifier
    )
    self.hover = 0  # (outside of rect)
    # test if x,y is inside the rect
    # change coordinates relative to self.x,self.y
    Dx = x - self.x
    Dy = y - self.y
    # rotate coordinates to be // to the rect
    rDx = Dx * math.cos(self.angle_rad) - Dy / self.paper_ratio * math.sin(
      self.angle_rad
    )
    rDy = Dx * self.paper_ratio * math.sin(self.angle_rad) + Dy * math.cos(
      self.angle_rad
    )
    Dw = settings.resize_area_width
    Dh = settings.resize_area_width * self.paper_ratio
    # Adapt size of resize/move areas for very small object
    Dw2 = min(Dw, (self.w + 2 * Dw) / 6)
    Dh2 = min(Dh, (self.h + 2 * Dh) / 6)
    if -Dw <= rDx <= self.w + Dw and -Dh <= rDy <= self.h + Dh:
      self.hover = 1000
      self.mousex = x
      self.mousey = y
      # Check locked properties
      if 'w' not in self.locked_props:
        if abs(rDx - Dw2 + Dw) <= Dw2:
          self.hover += 1  # left border
        elif abs(rDx - self.w + Dw2 - Dw) <= Dw2:
          self.hover += 2  # right border
      if 'h' not in self.locked_props:
        if abs(rDy - Dh2 + Dh) <= Dh2:
          self.hover += 10  # top border
        elif abs(rDy - self.h + Dh2 - Dh) <= Dh2:
          self.hover += 20  # bottom border
    return self.hover

  def selectCursor(self):
    """Choose which cursor should be drawn
    according to the mouse position and keyboard modifiers.
    """
    # TODO: Resizing cursors should be rotated with the same angle as the element.
    if self.metamod and not self.shiftmod:
      return QtCore.Qt.OpenHandCursor
    if self.hover == 1000:
      return QtCore.Qt.SizeAllCursor
    if self.hover == 1001 or self.hover == 1002:
      return QtCore.Qt.SizeHorCursor
    if self.hover == 1010 or self.hover == 1020:
      return QtCore.Qt.SizeVerCursor
    if self.hover == 1011 or self.hover == 1022:
      return QtCore.Qt.SizeFDiagCursor
    return QtCore.Qt.SizeBDiagCursor

  def get_ref(self):
    """Find the reference point (the fixed point when resizing the element)
    ref = opposite point to where the mouse is
    """
    if self.hover == 1001:
      ref = 'BD'
    elif self.hover == 1002:
      ref = 'AC'
    elif self.hover == 1010:
      ref = 'CD'
    elif self.hover == 1020:
      ref = 'AB'
    elif self.hover == 1011:
      ref = 'D'
    elif self.hover == 1012:
      ref = 'C'
    elif self.hover == 1021:
      ref = 'B'
    elif self.hover == 1022:
      ref = 'A'
    else:
      ref = 'center'
    return ref

  def which_point(self, pt_name):
    """Find to which point (A, B, C, or D) corresponds the left, right... guides"""
    if pt_name == 'left':
      return ['A', 'B', 'C', 'D'][
        argmin(
          [
            self.get_xguide('A'),
            self.get_xguide('B'),
            self.get_xguide('C'),
            self.get_xguide('D'),
          ]
        )
      ]
    if pt_name == 'right':
      return ['A', 'B', 'C', 'D'][
        argmax(
          [
            self.get_xguide('A'),
            self.get_xguide('B'),
            self.get_xguide('C'),
            self.get_xguide('D'),
          ]
        )
      ]
    if pt_name == 'top':
      return ['A', 'B', 'C', 'D'][
        argmin(
          [
            self.get_yguide('A'),
            self.get_yguide('B'),
            self.get_yguide('C'),
            self.get_yguide('D'),
          ]
        )
      ]
    if pt_name == 'bottom':
      return ['A', 'B', 'C', 'D'][
        argmax(
          [
            self.get_yguide('A'),
            self.get_yguide('B'),
            self.get_yguide('C'),
            self.get_yguide('D'),
          ]
        )
      ]
    return pt_name

  def relative_coords(self, point_name):
    """Relative coordinates of a point (0, 0.5, or 1)"""
    pt_name = self.which_point(point_name)
    if pt_name in ['AB', 'center', 'CD']:
      x = 1 / 2
    elif pt_name in ['B', 'BD', 'D']:
      x = 1
    else:
      x = 0
    if pt_name in ['AC', 'center', 'BD']:
      y = 1 / 2
    elif pt_name in ['C', 'CD', 'D']:
      y = 1
    else:
      y = 0
    return (x, y)

  def saveGeometry(self):
    """Initialisation before a move/resize/rotate event"""
    # Just remember the initial geometry of the element
    self.x0 = self.x
    self.y0 = self.y
    self.w0 = self.w
    self.h0 = self.h
    self.angle_deg0 = self.angle_deg
    self.angle_rad0 = self.angle_rad
    self.wheelx = 0
    self.wheely = 0
    self.hover0 = self.hover
    self.ref0 = self.get_ref()
    self.xg0 = self.get_xguide(self.ref0)
    self.yg0 = self.get_yguide(self.ref0)
    self.mousex0 = self.mousex - self.xg0
    self.mousey0 = self.mousey - self.yg0
    self.mouseangle0 = -math.atan2(self.mousey0, self.mousex0 * self.paper_ratio)
    if 'inactivated ratio' in self.locked_props:
      self.locked_props.remove('inactivated ratio')

  ###################### Moving
  # Set of functions that implement the moving of an element (guide magnetism...)
  def closest_xguide(self, extern_xguides):
    """Find the closest external guide (x-axis) to attract the element when moving it"""
    best_dist = float('inf')
    delta = 0
    for g in self.xguides:
      for eg in extern_xguides:
        dg = eg - g
        dist = abs(dg)
        if dist < best_dist and dist < settings.magnet_area_width:
          best_dist = dist
          delta = dg
    return delta

  def closest_yguide(self, extern_yguides):
    """Find the closest external guide (y-axis) to attract the element when moving it"""
    best_dist = float('inf')
    delta = 0
    for g in self.yguides:
      for eg in extern_yguides:
        dg = eg - g
        dist = abs(dg) / self.paper_ratio
        if dist < best_dist and dist < settings.magnet_area_width:
          best_dist = dist
          delta = dg
    return delta

  def move_x(self, Dx):
    """Move the element by Dx along x and recompute guides positions"""
    self.x = self.x0 + Dx
    self.refresh_xguides()

  def move_y(self, Dy):
    """Move the element by Dy along y and recompute guides positions"""
    self.y = self.y0 + Dy
    self.refresh_yguides()

  def magnet_move_x(self, Dx, dx, extern_xguides):
    """Move the element by Dx along x and get attracted if a guide is close enough"""
    # Check if the mouse as moved in the x direction since the last update
    if dx != 0:
      # Move
      self.move_x(Dx)
      # Find closest guide
      delta = self.closest_xguide(extern_xguides)
      # Move to guide if last mouse move was toward the guide
      if delta * dx >= 0:
        self.move_x(Dx + delta)

  def magnet_move_y(self, Dy, dy, extern_yguides):
    """Move the element by Dy along y and get attracted if a guide is close enough"""
    # Check if the mouse as moved in the y direction since the last update
    if dy != 0:
      # Move
      self.move_y(Dy)
      # Find closest guide
      delta = self.closest_yguide(extern_yguides)
      # Move to guide if last mouse move was toward the guide
      if delta * dy >= 0:
        self.move_y(Dy + delta)

  def magnet_move(self, Dx, Dy, dx, dy, extern_xguides, extern_yguides):
    """Move the element by Dx,Dy and get attracted by x/y guides if close enough"""
    self.magnet_move_x(Dx, dx, extern_xguides)
    self.magnet_move_y(Dy, dy, extern_yguides)

  ###################### Resizing
  # Set of functions that implement the resizing of an element (guide magnetism...)
  def resize_wh(self, Dw, Dh, ref):
    """Resize element by Dw, Dh using the reference ref
    (point of the element that stay fixed)
    """
    # Change size
    self.w = self.w0 + Dw
    self.h = self.h0 + Dh
    # Change position x,y of A depending on the reference point (ref)
    rDx = -Dw * self.relative_coords(ref)[0]
    rDy = -Dh * self.relative_coords(ref)[1]
    self.x = (
      self.x0
      + math.cos(self.angle_rad) * rDx
      + math.sin(self.angle_rad) * rDy / self.paper_ratio
    )
    self.y = (
      self.y0
      - math.sin(self.angle_rad) * rDx * self.paper_ratio
      + math.cos(self.angle_rad) * rDy
    )

  def closest_whguide_lratio(self, extern_xguides, extern_yguides, ref):
    """Find the closest guide when resizing with locked ratio"""
    # Reference point coordinates
    ref_coords = self.relative_coords(ref)
    best_dist = float('inf')
    deltaw = 0
    deltah = 0
    # x guides
    for gn, g in zip(self.xguides_names, self.xguides):
      # guide coordinates
      g_coords = self.relative_coords(gn)
      # width/height coefficients (rotation + relative position of ref and guide)
      cw = (g_coords[0] - ref_coords[0]) * math.cos(self.angle_rad)
      ch = (g_coords[1] - ref_coords[1]) * math.sin(self.angle_rad)
      det = cw * self.w0 + ch * self.h0 / self.paper_ratio
      if abs(det) < settings.epsilon:
        continue
      cw = self.w0 / det
      ch = self.h0 / self.paper_ratio / det
      for eg in extern_xguides:
        # Distance to the external guide (x-axis)
        dgx = eg - g
        # Distance in terms of width/height changes
        dgw = cw * dgx
        dgh = ch * dgx
        dist = math.sqrt(dgw**2 + dgh**2)
        dgh *= self.paper_ratio
        # Compare distance to the best distance
        if (
          self.w + dgw >= self.minw
          and self.h + dgh >= self.minh
          and dist < best_dist
          and dist < settings.magnet_area_width
        ):
          best_dist = dist
          deltaw = dgw
          deltah = dgh
    # y guides (same as x)
    for gn, g in zip(self.yguides_names, self.yguides):
      g_coords = self.relative_coords(gn)
      cw = -(g_coords[0] - ref_coords[0]) * math.sin(self.angle_rad)
      ch = (g_coords[1] - ref_coords[1]) * math.cos(self.angle_rad)
      det = cw * self.w0 + ch * self.h0 / self.paper_ratio
      if abs(det) < settings.epsilon:
        continue
      cw = self.w0 / det
      ch = self.h0 / self.paper_ratio / det
      for eg in extern_yguides:
        dgy = (eg - g) / self.paper_ratio
        dgw = cw * dgy
        dgh = ch * dgy
        dist = math.sqrt(dgw**2 + dgh**2)
        dgh *= self.paper_ratio
        if (
          self.w + dgw >= self.minw
          and self.h + dgh >= self.minh
          and dist < best_dist
          and dist < settings.magnet_area_width
        ):
          best_dist = dist
          deltaw = dgw
          deltah = dgh
    # Return the change in width/height to be aligned with the closest guide
    # (return (0,0) if no guide is close enough)
    return (deltaw, deltah)

  def closest_whguide_lwidth(self, extern_xguides, extern_yguides, ref):
    """Find the closest guide when resizing with locked width"""
    # Reference point coordinates
    ref_coords = self.relative_coords(ref)
    best_dist = float('inf')
    deltah = 0
    # x guides
    for gn, g in zip(self.xguides_names, self.xguides):
      g_coords = self.relative_coords(gn)
      ch = (g_coords[1] - ref_coords[1]) * math.sin(self.angle_rad)
      if abs(ch) < settings.epsilon:
        continue
      for eg in extern_xguides:
        dgx = eg - g
        dgh = dgx / ch
        dist = abs(dgh)
        dgh *= self.paper_ratio
        if (
          self.h + dgh >= self.minh
          and dist < best_dist
          and dist < settings.magnet_area_width
        ):
          best_dist = dist
          deltah = dgh
    # y guides
    for gn, g in zip(self.yguides_names, self.yguides):
      g_coords = self.relative_coords(gn)
      ch = (g_coords[1] - ref_coords[1]) * math.cos(self.angle_rad)
      if abs(ch) < settings.epsilon:
        continue
      for eg in extern_yguides:
        dgy = (eg - g) / self.paper_ratio
        dgh = dgy / ch
        dist = abs(dgh)
        dgh *= self.paper_ratio
        if (
          self.h + dgh >= self.minh
          and dist < best_dist
          and dist < settings.magnet_area_width
        ):
          best_dist = dist
          deltah = dgh
    return (0, deltah)

  def closest_whguide_lheight(self, extern_xguides, extern_yguides, ref):
    """Find the closest guide when resizing with locked height"""
    # Reference point coordinates
    ref_coords = self.relative_coords(ref)
    best_dist = float('inf')
    deltaw = 0
    # x guides
    for gn, g in zip(self.xguides_names, self.xguides):
      g_coords = self.relative_coords(gn)
      cw = (g_coords[0] - ref_coords[0]) * math.cos(self.angle_rad)
      if abs(cw) < settings.epsilon:
        continue
      for eg in extern_xguides:
        dgx = eg - g
        dgw = dgx / cw
        dist = abs(dgw)
        if (
          self.w + dgw >= self.minw
          and dist < best_dist
          and dist < settings.magnet_area_width
        ):
          best_dist = dist
          deltaw = dgw
    # y guides
    for gn, g in zip(self.yguides_names, self.yguides):
      g_coords = self.relative_coords(gn)
      cw = -(g_coords[0] - ref_coords[0]) * math.sin(self.angle_rad)
      if abs(cw) < settings.epsilon:
        continue
      for eg in extern_yguides:
        dgy = (eg - g) / self.paper_ratio
        dgw = dgy / cw
        dist = abs(dgw)
        if (
          self.w + dgw >= self.minw
          and dist < best_dist
          and dist < settings.magnet_area_width
        ):
          best_dist = dist
          deltaw = dgw
    return (deltaw, 0)

  def optimize_deltawh(self, dxy, cw, ch):
    # Minimize d**2 = dw**2 + dh**2
    # under the conditions:
    # 1) cw*dw + ch*dh = dxy
    # 2) w + dw > minw
    # 3) h + dh > minh
    mdw = self.minw - self.w
    mdh = self.minh - self.h
    # Unsatured case
    lax = dxy / (cw**2 + ch**2)
    dw = lax * cw
    dh = lax * ch
    # dw saturation
    if dw < mdw:
      if abs(ch) < settings.epsilon:
        return None
      dw = mdw
      dh = (dxy - cw * dw) / ch
      # double saturation
      if dh < mdh:
        dh = mdh
        if abs(cw * dw + ch * dh - dxy) > settings.epsilon:
          return None
    # dh saturation
    elif dh < mdh:
      if abs(cw) < settings.epsilon:
        return None
      dh = mdh
      dw = (dxy - ch * dh) / cw
      # double saturation
      if dw < mdw:
        dw = mdw
        if abs(cw * dw + ch * dh - dxy) > settings.epsilon:
          return None
    return (dw, dh)

  def closest_whguide_nol(self, extern_xguides, extern_yguides, ref):
    """Find the closest guide when resizing without any locked property"""
    # Reference point coordinates
    ref_coords = self.relative_coords(ref)
    # x guides
    best_distx = float('inf')
    for gn, g in zip(self.xguides_names, self.xguides):
      g_coords = self.relative_coords(gn)
      cw = (g_coords[0] - ref_coords[0]) * math.cos(self.angle_rad)
      ch = (g_coords[1] - ref_coords[1]) * math.sin(self.angle_rad)
      if cw**2 + ch**2 < settings.epsilon:
        continue
      for eg in extern_xguides:
        dgx = eg - g
        # Optimize the change in w and h
        # to align with the external guide by minimizing dist**2 = dgw**2+dgh**2
        optim = self.optimize_deltawh(dgx, cw, ch)
        if optim is None:
          continue
        dgw = optim[0]
        dgh = optim[1]
        dist = math.sqrt(dgw**2 + dgh**2)
        if dist < best_distx and dist < settings.magnet_area_width:
          best_distx = dist
          deltax = dgx
          cwx = cw
          chx = ch
          deltawx = dgw
          deltahx = dgh * self.paper_ratio
    # y guides
    best_disty = float('inf')
    for gn, g in zip(self.yguides_names, self.yguides):
      g_coords = self.relative_coords(gn)
      cw = -(g_coords[0] - ref_coords[0]) * math.sin(self.angle_rad)
      ch = (g_coords[1] - ref_coords[1]) * math.cos(self.angle_rad)
      if cw**2 + ch**2 < settings.epsilon**2:
        continue
      for eg in extern_yguides:
        dgy = (eg - g) / self.paper_ratio
        optim = self.optimize_deltawh(dgy, cw, ch)
        if optim is None:
          continue
        dgw = optim[0]
        dgh = optim[1]
        dist = math.sqrt(dgw**2 + dgh**2)
        if dist < best_disty and dist < settings.magnet_area_width:
          best_disty = dist
          deltay = dgy
          cwy = cw
          chy = ch
          deltawy = dgw
          deltahy = dgh * self.paper_ratio
    # Try to align with both x and y guides if possible
    if best_distx < settings.magnet_area_width:
      if best_disty < settings.magnet_area_width:
        # There is a close enough guide for both x and y
        # So we try to align both
        det = cwx * chy - cwy * chx
        if abs(det) > settings.epsilon:
          deltaw = (chy * deltax - chx * deltay) / det
          deltah = (-cwy * deltax + cwx * deltay) / det
          dist = math.sqrt(deltaw**2 + deltah**2)
          # Check if aligning both x,y is not too far
          if dist < settings.magnet_area_width:
            return (deltaw, deltah * self.paper_ratio)
        # When not possible to align both, align with the closest
        if best_disty < best_distx:
          return (deltawy, deltahy)
      return (deltawx, deltahx)
    if best_disty < settings.magnet_area_width:
      return (deltawy, deltahy)
    # No guide is close enough
    return (0, 0)

  def closest_whguide(self, extern_xguides, extern_yguides, ref, locked_props):
    """Find the closest guide when resizing"""
    # Check the locked properties
    if 'ratio' in locked_props:
      return self.closest_whguide_lratio(extern_xguides, extern_yguides, ref)
    if 'w' in locked_props:
      return self.closest_whguide_lwidth(extern_xguides, extern_yguides, ref)
    if 'h' in locked_props:
      return self.closest_whguide_lheight(extern_xguides, extern_yguides, ref)
    return self.closest_whguide_nol(extern_xguides, extern_yguides, ref)

  def magnet_resize_wh(self, Dw, Dh, dw, dh, ref, extern_xguides, extern_yguides):
    """Resize the element by Dw, Dh and get attracted if a guide is close enough"""
    if dw != 0 or dh != 0:
      Dw = max(Dw, self.minw - self.w0)
      Dh = max(Dh, self.minh - self.h0)
      self.resize_wh(Dw, Dh, ref)
      self.refresh_xguides()
      self.refresh_yguides()
      locked_props = list(self.locked_props)
      if Dw == 0 and 'ratio' not in locked_props:
        locked_props.append('w')
      if Dh == 0 and 'ratio' not in locked_props:
        locked_props.append('h')
      deltaw, deltah = self.closest_whguide(
        extern_xguides, extern_yguides, ref, locked_props
      )
      if deltaw * dw + deltah * dh / self.paper_ratio >= 0:
        self.resize_wh(Dw + deltaw, Dh + deltah, ref)

  def magnet_resize(self, Dx, Dy, dx, dy, extern_xguides, extern_yguides):
    """Resize the element and get attracted if a guide is close enough,
    according to mouse move
    """
    Dw = (
      math.cos(self.angle_rad) * Dx - math.sin(self.angle_rad) * Dy / self.paper_ratio
    )
    dw = (
      math.cos(self.angle_rad) * dx - math.sin(self.angle_rad) * dy / self.paper_ratio
    )
    Dh = (
      math.sin(self.angle_rad) * Dx * self.paper_ratio + math.cos(self.angle_rad) * Dy
    )
    dh = (
      math.sin(self.angle_rad) * dx * self.paper_ratio + math.cos(self.angle_rad) * dy
    )
    if self.hover0 == 1001:
      Dw *= -1
      dw *= -1
      Dh = Dw * self.h0 / self.w0 if 'ratio' in self.locked_props else 0
      dh = dw * self.h0 / self.w0 if 'ratio' in self.locked_props else 0
      ref = 'BD'
    elif self.hover0 == 1002:
      Dh = Dw * self.h0 / self.w0 if 'ratio' in self.locked_props else 0
      dh = dw * self.h0 / self.w0 if 'ratio' in self.locked_props else 0
      ref = 'AC'
    elif self.hover0 == 1010:
      Dh *= -1
      dh *= -1
      Dw = Dh * self.w0 / self.h0 if 'ratio' in self.locked_props else 0
      dw = dh * self.w0 / self.h0 if 'ratio' in self.locked_props else 0
      ref = 'CD'
    elif self.hover0 == 1020:
      Dw = Dh * self.w0 / self.h0 if 'ratio' in self.locked_props else 0
      dw = dh * self.w0 / self.h0 if 'ratio' in self.locked_props else 0
      ref = 'AB'
    else:
      if self.hover0 == 1011:
        Dw *= -1
        dw *= -1
        Dh *= -1
        dh *= -1
        ref = 'D'
      elif self.hover0 == 1012:
        Dh *= -1
        dh *= -1
        ref = 'C'
      elif self.hover0 == 1021:
        Dw *= -1
        dw *= -1
        ref = 'B'
      elif self.hover0 == 1022:
        ref = 'A'
      if 'ratio' in self.locked_props:
        if Dh * self.w0 < Dw * self.h0:
          Dh = Dw * self.h0 / self.w0
          dh = dw * self.h0 / self.w0
        else:
          Dw = Dh * self.w0 / self.h0
          dw = dh * self.w0 / self.h0

    self.magnet_resize_wh(Dw, Dh, dw, dh, ref, extern_xguides, extern_yguides)

  def rotate(self, Dx, Dy, dx, dy, extern_xguides, extern_yguides):
    """Rotate the element according to mouse move"""
    dangle = (
      -math.atan2(self.mousey0 + Dy, (self.mousex0 + Dx) * self.paper_ratio)
      - self.mouseangle0
    )
    prec = settings.rotate_prec_deg / 180 * math.pi
    dangle = prec * round(dangle / prec)
    self.angle_rad = (self.angle_rad0 + dangle + math.pi) % (2 * math.pi) - math.pi
    self.angle_deg = self.angle_rad * 180 / math.pi
    self.x = self.x0
    self.y = self.y0
    self.x += self.xg0 - self.get_xguide(self.ref0)
    self.y += self.yg0 - self.get_yguide(self.ref0)

  def change_geom(self, Dx, Dy, dx, dy, extern_xguides, extern_yguides):
    """Change the geometry of the element according to mouse move.
    Decide wether to move/resize/rotate depending on mouse position and key modifiers.
    """
    # If Meta is pressed (at the beginning) -> rotation
    if self.metamod and not self.shiftmod:
      self.rotate(Dx, Dy, dx, dy, extern_xguides, extern_yguides)
    elif self.hover0 == 1000:
      self.magnet_move(Dx, Dy, dx, dy, extern_xguides, extern_yguides)
    else:
      # If Shift is pressed -> do not conserve ratio (can change during resizing)
      if QtWidgets.QApplication.queryKeyboardModifiers() & QtCore.Qt.ShiftModifier:
        if 'ratio' in self.locked_props:
          self.locked_props.remove('ratio')
          self.locked_props.append('inactivated ratio')
      elif 'inactivated ratio' in self.locked_props:
        self.locked_props.remove('inactivated ratio')
        self.locked_props.append('ratio')
      self.magnet_resize(Dx, Dy, dx, dy, extern_xguides, extern_yguides)
    self.refresh_xguides()
    self.refresh_yguides()

  def clean_imgs(self):
    """Clean all preview images from the element."""
    self.imgs = None


########################################################### TEXT
class Text(Element):
  """Defines a text block"""

  def __init__(self, *args, **kwargs):
    """Initialisation"""
    super().__init__()
    if len(args) > 0 and type(args[0]) is ET.Element:
      self.readxml(*args, **kwargs)
    else:
      self.init(*args, **kwargs)
    self.refresh_xguides()
    self.refresh_yguides()

  def init(
    self,
    x=0,
    y=0,
    w=1,
    h=1,
    minw=0,
    minh=0,
    angle_deg=0,
    pagesCMD='',
    pagesList=(),
    imgs=None,
    hover=0,
    selected=False,
    group=None,
    before='',
    xguides_names=('left', 'center', 'right'),
    yguides_names=('bottom', 'center', 'top'),
    paper_ratio=1,
    current_align_x=(),
    current_align_y=(),
    locked_props=(),
    text='',
    align='left',
  ):
    """Initialisation from parameters"""
    super().init(
      x,
      y,
      w,
      h,
      minw,
      minh,
      angle_deg,
      pagesCMD,
      pagesList,
      imgs,
      hover,
      selected,
      group,
      before,
      xguides_names,
      yguides_names,
      paper_ratio,
      current_align_x,
      current_align_y,
      locked_props,
    )
    # Text content
    self.text = text
    # Alignment of the text in the text block (left,center,right)
    self.align = align

  def readxml(self, xmlElement, npages, slide_imgs, paper_ratio):
    """Initialisation from xml file"""
    super().readxml(xmlElement, npages, slide_imgs, paper_ratio)
    self.text = striplines(xmlElement.get('text').strip(), 6)
    self.align = xmlElement.get('align')
    self.xguides_names = ['left', 'center', 'right']
    self.yguides_names = ['bottom', 'center', 'top']
    self.minh = float(xmlElement.get('minh'))

  def copy(self):
    """Deep copy function"""
    return Text(
      self.x,
      self.y,
      self.w,
      self.h,
      self.minw,
      self.minh,
      self.angle_deg,
      self.pagesCMD,
      self.pagesList,
      self.imgs,
      self.hover,
      self.selected,
      self.group,
      self.before,
      self.xguides_names,
      self.yguides_names,
      self.paper_ratio,
      self.current_align_x,
      self.current_align_y,
      self.locked_props,
      self.text,
      self.align,
    )

  def writeTeX(self, groups):
    """Write the TeX extract from the element properties"""
    # Try and put a correct indenting
    tex = ''
    if self.before.strip():
      tex += spacelines(self.before.strip(), 4) + '\n'
    tex += '    \\txt{'
    tex += f'{self.x:.4f},{self.y:.4f},{self.w:.4f}'
    if self.pagesCMD not in ('', '1-'):
      tex += f';pages={self.pagesCMD}'
    if self.align != 'left':
      tex += f';align={self.align}'
    if self.angle_deg != 0:
      tex += f';angle={self.angle_deg:.0f}'
    if self.group:
      tex += f';group={groups.index(self.group) + 1}'
    if self.minh < self.h:
      tex += f';height={self.h:.4f}'
    tex += '}{'
    if '\n' in self.text.strip():
      tex += '\n' + spacelines(self.text.strip(), 6) + '\n    }'
    else:
      tex += self.text.strip() + '}'
    return tex

  def edit(self, parentwindow):
    """Launch the PropertiesEditor (see editor.py) to edit the Text properties."""
    alignarray = ['left', 'center', 'right']
    # Initial values of props (before editing)
    init_values = [
      self.x,
      self.y,
      self.w,
      self.h,
      self.angle_deg,
      self.text,
      alignarray.index(self.align),
      self.pagesCMD,
      ','.join(self.xguides_names),
      ','.join(self.yguides_names),
    ]

    # Define BedWidget for each prop (see editor.py)
    bwx = BedDoubleSpinBox(init_values[0], -1, 2, 0.01, 4, label='x')
    bwy = BedDoubleSpinBox(init_values[1], -1, 2, 0.01, 4, label='y')
    bww = BedDoubleSpinBox(init_values[2], self.minw, 2, 0.01, 4, label='w')
    bwh = BedDoubleSpinBox(init_values[3], self.minh, 2, 0.01, 4, label='h')
    bwangle = BedDoubleSpinBox(init_values[4], -180, 360, 5, 2, label=self.tr('Angle'))
    bwtext = BedAdjustTextEdit(init_values[5], label=self.tr('Text'), highlight=True)
    bwalign = BedComboBox(
      init_values[6], [self.tr(al) for al in alignarray], label=self.tr('Align.')
    )
    bwpages = BedLineEdit(init_values[7], label=self.tr('Pages'))
    bwxguides = BedLineEdit(init_values[8], label=self.tr('x guides'))
    bwyguides = BedLineEdit(init_values[9], label=self.tr('y guides'))
    bedwidgets = [
      bwx,
      bwy,
      bww,
      bwh,
      bwangle,
      bwtext,
      bwalign,
      bwpages,
      bwxguides,
      bwyguides,
    ]
    values = PropertiesEditor.getValues(
      parentwindow, bedwidgets, settings, 'text', self.tr('Text')
    )
    # Check if values have changed
    if values:
      # Update properties
      self.x = values[0]
      self.y = values[1]
      self.w = values[2]
      self.h = values[3]
      self.angle_deg = values[4]
      self.angle_rad = values[4] * math.pi / 180
      self.text = values[5]
      self.align = alignarray[values[6]]
      self.pagesCMD = values[7]
      self.xguides_names = values[8].split(',')
      self.yguides_names = values[9].split(',')
      self.refresh_xguides()
      self.refresh_yguides()
      return True
    return False


########################################################### IMAGE
class Image(Element):
  """Defines an image"""

  def __init__(self, *args, **kwargs):
    """Initialisation"""
    super().__init__()
    if len(args) > 0 and type(args[0]) is ET.Element:
      self.readxml(*args, **kwargs)
    else:
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
    pagesCMD='',
    pagesList=(),
    imgs=None,
    hover=0,
    selected=False,
    group=None,
    before='',
    xguides_names=('left', 'center', 'right'),
    yguides_names=('bottom', 'center', 'top'),
    paper_ratio=1,
    current_align_x=(),
    current_align_y=(),
    locked_props=(),
    filename='',
    origratio=None,
    trim=(0, 0, 0, 0),
    trim_init=(0, 0, 0, 0),
    link='',
    opt='',
  ):
    """Initialisation from parameters"""
    super().init(
      x,
      y,
      w,
      h,
      minw,
      minh,
      angle_deg,
      pagesCMD,
      pagesList,
      imgs,
      hover,
      selected,
      group,
      before,
      xguides_names,
      yguides_names,
      paper_ratio,
      current_align_x,
      current_align_y,
      locked_props,
    )
    self.filename = filename
    self.trim = list(trim)
    # default widht / height ratio
    if origratio:
      self.origratio = origratio
    else:
      self.origratio = w / h
    # Check if the width/height ratio is locked to the default value
    if locked_props is None and self.isOrigratio():
      self.locked_props = ['ratio']
    self.trim_init = list(trim_init)
    self.link = link
    self.opt = opt

  def readxml(self, xmlElement, npages, slide_imgs, paper_ratio):
    """Initialisation from xml file"""
    super().readxml(xmlElement, npages, slide_imgs, paper_ratio)
    self.filename = xmlElement.get('name')
    self.origratio = float(xmlElement.get('origratio'))
    self.trim = [float(x) for x in xmlElement.get('trim').split(' ')]
    self.link = xmlElement.get('link')
    self.locked_props = ['ratio'] if xmlElement.get('isorigratio') == '1' else []
    self.xguides_names = ['left', 'center', 'right']
    self.yguides_names = ['bottom', 'center', 'top']
    self.trim_init = list(self.trim)
    self.opt = xmlElement.get('ukoa')
    self.minw = settings.epsilon
    self.minh = settings.epsilon

  def copy(self):
    """Deep copy function"""
    return Image(
      self.x,
      self.y,
      self.w,
      self.h,
      self.minw,
      self.minh,
      self.angle_deg,
      self.pagesCMD,
      self.pagesList,
      self.imgs,
      self.hover,
      self.selected,
      self.group,
      self.before,
      self.xguides_names,
      self.yguides_names,
      self.paper_ratio,
      self.current_align_x,
      self.current_align_y,
      self.locked_props,
      self.filename,
      self.origratio,
      self.trim,
      self.trim_init,
      self.link,
      self.opt,
    )

  def writeTeX(self, groups):
    """Write the TeX extract from the element properties"""
    # Try and put a correct indenting
    tex = ''
    if self.before.strip():
      tex += spacelines(self.before.strip(), 4) + '\n'
    tex += '    \\img{'
    tex += f'{self.x:.4f},{self.y:.4f},{self.w:.4f}'
    if not self.isOrigratio():
      tex += f';height={self.h:.4f}'
    if self.angle_deg != 0:
      tex += f';angle={self.angle_deg:.0f}'
    if self.trim != [0, 0, 0, 0]:
      tex += (
        f';trim={self.trim[0]:.4f} {self.trim[1]:.4f} '
        f'{self.trim[2]:.4f} {self.trim[3]:.4f}'
      )
    if self.link != '':
      tex += f';link={self.link}'
    if self.pagesCMD not in ('', '1-'):
      tex += f';pages={self.pagesCMD}'
    if self.opt:
      tex += f';{self.opt}'
    if self.group:
      tex += f';group={groups.index(self.group) + 1}'
    tex += '}{' + self.filename.strip() + '}'
    return tex

  def draw(self, framepage, painter, isgroup=False):
    """Drawing function (called by the painter, see painter.py)"""
    # Add cropping to the super function
    # Check if a preview is available for the image
    if self.imgs and framepage < len(self.imgs) and self.imgs[framepage]:
      # If available crop it
      img = self.imgs[framepage]
      x = (
        (self.trim[0] - self.trim_init[0])
        / (1 - self.trim_init[0] - self.trim_init[2])
        * img.width()
      )
      y = (
        (self.trim[3] - self.trim_init[3])
        / (1 - self.trim_init[1] - self.trim_init[3])
        * img.height()
      )
      w = round(
        (1 - self.trim[0] - self.trim[2])
        / (1 - self.trim_init[0] - self.trim_init[2])
        * img.width()
      )
      h = round(
        (1 - self.trim[1] - self.trim[3])
        / (1 - self.trim_init[1] - self.trim_init[3])
        * img.height()
      )
      ml = max(self.trim[0], self.trim_init[0])
      mr = max(self.trim[2], self.trim_init[2])
      mt = max(self.trim[3], self.trim_init[3])
      mb = max(self.trim[1], self.trim_init[1])
      sw = (1 - ml - mr) / (1 - self.trim_init[0] - self.trim_init[2]) * img.width()
      sh = (1 - mt - mb) / (1 - self.trim_init[1] - self.trim_init[3]) * img.height()
      sx = max(0, x)
      sy = max(0, y)
      tx = max(0, -x)
      ty = max(0, -y)
      srect = QtCore.QRectF(sx, sy, sw, sh)
      trect = QtCore.QRectF(tx, ty, sw, sh)
      modimg = QtGui.QImage(w, h, img.format())
      modimg.fill(QtGui.QColor(255, 255, 255))
      qp = QtGui.QPainter(modimg)
      qp.drawImage(trect, img, srect)
      qp.end()
      # Draw using the super function
      super().draw(framepage, painter, isgroup, img=modimg)
    else:
      # Preview not available
      # Fill the image with gray using the super() function
      super().draw(framepage, painter, isgroup)

  def saveGeometry(self):
    """Initialisation before a move/resize/rotate event"""
    # Just remember the initial geometry
    super().saveGeometry()
    self.trim0 = list(self.trim)

  def isOrigratio(self):
    """Check if the current w/h ratio preserve the original ratio"""
    # Possible image cropping need to be take into account
    return (
      abs(
        self.w * (1 - self.trim[1] - self.trim[3])
        - self.h * (1 - self.trim[0] - self.trim[2]) * self.origratio
      )
      < settings.epsilon
    )

  def crop(self, Dx, Dy, extern_xguides, extern_yguides):
    """Crop the image (with mouse)"""
    # Full image size (without any cropping)
    wtot = self.w0 / (1 - self.trim0[0] - self.trim0[2])
    htot = self.h0 / (1 - self.trim0[1] - self.trim0[3])
    rDx = (
      math.cos(self.angle_rad) * Dx - math.sin(self.angle_rad) * Dy / self.paper_ratio
    )
    rDy = (
      math.sin(self.angle_rad) * Dx * self.paper_ratio + math.cos(self.angle_rad) * Dy
    )
    prec = settings.mouse_crop_prec
    cropmaxw = 1 - self.minw / wtot
    cropmaxh = 1 - self.minh / htot
    # Check which side we want to crop (mouse position)
    if self.hover0 % 10 == 1:
      self.trim[0] = self.trim0[0] + rDx / wtot
      if prec > 0:
        self.trim[0] = round(self.trim[0] / prec) * prec
      self.trim[0] = min(max(self.trim[0], 0), cropmaxw - self.trim[2])
    elif self.hover0 % 10 == 2:
      self.trim[2] = self.trim0[2] - rDx / wtot
      if prec > 0:
        self.trim[2] = round(self.trim[2] / prec) * prec
      self.trim[2] = min(max(self.trim[2], 0), cropmaxw - self.trim[0])
    if self.hover0 % 100 - self.hover0 % 10 == 10:
      self.trim[3] = self.trim0[3] + rDy / htot
      if prec > 0:
        self.trim[3] = round(self.trim[3] / prec) * prec
      self.trim[3] = min(max(self.trim[3], 0), cropmaxh - self.trim[1])
    elif self.hover0 % 100 - self.hover0 % 10 == 20:
      self.trim[1] = self.trim0[1] - rDy / htot
      if prec > 0:
        self.trim[1] = round(self.trim[1] / prec) * prec
      self.trim[1] = min(max(self.trim[1], 0), cropmaxh - self.trim[3])
    # Update w,h,x,y accordingly
    self.w = wtot * (1 - self.trim[0] - self.trim[2])
    self.h = htot * (1 - self.trim[1] - self.trim[3])
    rdx = wtot * (self.trim[0] - self.trim0[0])
    rdy = htot * (self.trim[3] - self.trim0[3])
    self.x = (
      self.x0
      + math.cos(self.angle_rad) * rdx
      + math.sin(self.angle_rad) * rdy / self.paper_ratio
    )
    self.y = (
      self.y0
      - math.sin(self.angle_rad) * rdx * self.paper_ratio
      + math.cos(self.angle_rad) * rdy
    )

  def change_geom(self, Dx, Dy, dx, dy, extern_xguides, extern_yguides):
    """Change the geometry of the element according to mouse move.
    Decide wether to move/resize/rotate/crop
    depending on mouse position and key modifiers.
    """
    # Add cropping possibility to the super function
    if self.shiftmod and self.metamod and self.hover0 > 1000:
      self.crop(Dx, Dy, extern_xguides, extern_yguides)
      self.refresh_xguides()
      self.refresh_yguides()
    else:
      super().change_geom(Dx, Dy, dx, dy, extern_xguides, extern_yguides)

  def edit(self, parentwindow):
    """Launch the PropertiesEditor (see editor.py) to edit the Image properties."""
    # Initial values of props (before editing)
    init_values = [
      self.x,
      self.y,
      self.w,
      self.h,
      ('ratio' in self.locked_props),
      None,
      self.angle_deg,
      self.trim[0],
      self.trim[1],
      self.trim[2],
      self.trim[3],
      self.filename,
      None,
      self.link,
      self.opt,
      self.pagesCMD,
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
      tl = parent.bedwidgets[7].value()
      tb = parent.bedwidgets[8].value()
      tr = parent.bedwidgets[9].value()
      tt = parent.bedwidgets[10].value()
      h = (1 - tb - tt) / (1 - tl - tr) * w / self.origratio
      parent.bedwidgets[3].setValue(h)
      parent.changing = False

    def oCtl(parent):
      """Crop left -> update x,y,w"""
      parent.changing = True
      x = parent.bedwidgets[0].value()
      y = parent.bedwidgets[1].value()
      w = parent.bedwidgets[2].value()
      angledeg = parent.bedwidgets[6].value()
      anglerad = angledeg * math.pi / 180
      tl = parent.bedwidgets[7].value()
      tr = parent.bedwidgets[9].value()
      prevtl = parent.bedwidgets[7].prev_value
      nw = w * (1 - tl - tr) / (1 - prevtl - tr)
      if nw < self.minw:
        nw = self.minw
        tl = 1 - tr - nw / w * (1 - prevtl - tr)
        parent.bedwidgets[7].setValue(tl)
      dw = nw - w
      x -= dw * math.cos(anglerad)
      y += dw * math.sin(anglerad) * self.paper_ratio
      parent.bedwidgets[0].setValue(x)
      parent.bedwidgets[1].setValue(y)
      parent.bedwidgets[2].setValue(nw)
      parent.changing = False

    def oCtb(parent):
      """Crop bottom -> update x,y,h"""
      parent.changing = True
      x = parent.bedwidgets[0].value()
      y = parent.bedwidgets[1].value()
      h = parent.bedwidgets[3].value()
      angledeg = parent.bedwidgets[6].value()
      anglerad = angledeg * math.pi / 180
      tb = parent.bedwidgets[8].value()
      tt = parent.bedwidgets[10].value()
      prevtb = parent.bedwidgets[8].prev_value
      nh = h * (1 - tb - tt) / (1 - prevtb - tt)
      if nh < self.minh:
        nh = self.minh
        tb = 1 - tt - nh / h * (1 - prevtb - tt)
        parent.bedwidgets[8].setValue(tb)
      dh = nh - h
      x -= dh * math.sin(anglerad) / self.paper_ratio
      y -= dh * math.cos(anglerad)
      parent.bedwidgets[0].setValue(x)
      parent.bedwidgets[1].setValue(y)
      parent.bedwidgets[3].setValue(nh)
      parent.changing = False

    def oCtr(parent):
      """Crop right -> update x,y,w"""
      parent.changing = True
      w = parent.bedwidgets[2].value()
      tl = parent.bedwidgets[7].value()
      tr = parent.bedwidgets[9].value()
      prevtr = parent.bedwidgets[9].prev_value
      nw = w * (1 - tl - tr) / (1 - tl - prevtr)
      if nw < self.minw:
        nw = self.minw
        tr = 1 - tl - nw / w * (1 - prevtr - tl)
        parent.bedwidgets[9].setValue(tr)
      parent.bedwidgets[2].setValue(nw)
      parent.changing = False

    def oCtt(parent):
      """Crop top -> update x,y,h"""
      parent.changing = True
      h = parent.bedwidgets[3].value()
      tb = parent.bedwidgets[8].value()
      tt = parent.bedwidgets[10].value()
      prevtt = parent.bedwidgets[10].prev_value
      nh = h * (1 - tb - tt) / (1 - tb - prevtt)
      if nh < self.minh:
        nh = self.minh
        tt = 1 - tb - nh / h * (1 - prevtt - tb)
        parent.bedwidgets[10].setValue(tt)
      parent.bedwidgets[3].setValue(nh)
      parent.changing = False

    def oCbrowse(parent):
      """Image filename -> recompute relative path"""
      parent.changing = True
      filename = QtWidgets.QFileDialog.getOpenFileName(
        parent, self.tr('Open Image'), '.', 'Image (*.png *.jpg *.jpeg *.pdf)'
      )[0]
      if filename != '':
        # Compute the relative path of image (vs tex file path)
        # First separate folder and filename
        spFolderFile = re.split(r'/', filename)
        folder = r'/'.join(spFolderFile[:-1])
        if folder == '':
          folder = os.getcwd()
        folder += '/'
        # Check if there is a tex file folder defined
        if parentwindow.folder:
          # Get it
          texfolder = parentwindow.folder
          # Find the common prefix of the tex and image folder
          prefix = os.path.commonprefix([folder, texfolder])
          prefix = '/'.join(prefix.split(r'/')[:-1]) + '/'
          # Remove this common prefix from both paths
          folder = folder[len(prefix) :]
          texfolder = texfolder[len(prefix) :]
          # Add the necessary "../" at the beginning of the image path
          # To create the relative path
          for _ in texfolder.split('/')[1:]:
            folder = '../' + folder
        # Put the relative folder + filename without extension in the lineEdit
        spNameExt = re.split(r'\.', spFolderFile[-1])
        parent.bedwidgets[11].setValue(folder + '.'.join(spNameExt[:-1]))
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
    bwtriml = BedDoubleSpinBox(
      init_values[7], 0, 1, 0.01, 4, label=self.tr('Crop left'), onChange=oCtl
    )
    bwtrimb = BedDoubleSpinBox(
      init_values[8], 0, 1, 0.01, 4, label=self.tr('Crop bottom'), onChange=oCtb
    )
    bwtrimr = BedDoubleSpinBox(
      init_values[9], 0, 1, 0.01, 4, label=self.tr('Crop right'), onChange=oCtr
    )
    bwtrimt = BedDoubleSpinBox(
      init_values[10], 0, 1, 0.01, 4, label=self.tr('Crop top'), onChange=oCtt
    )
    bwfilename = BedLineEdit(init_values[11], label=self.tr('Filename'))
    bwbrowse = BedPushButton(
      label=' ', buttonlabel=self.tr('Browse'), onChange=oCbrowse
    )
    bwlink = BedLineEdit(init_values[13], label=self.tr('Link'))
    bwopt = BedLineEdit(init_values[14], label=self.tr('Opt. args.'))
    bwpages = BedLineEdit(init_values[15], label=self.tr('Pages'))
    bwxguides = BedLineEdit(init_values[16], label=self.tr('x guides'))
    bwyguides = BedLineEdit(init_values[17], label=self.tr('y guides'))
    bedwidgets = [
      bwx,
      bwy,
      bww,
      bwh,
      bwlock,
      bwreset,
      bwangle,
      bwtriml,
      bwtrimb,
      bwtrimr,
      bwtrimt,
      bwfilename,
      bwbrowse,
      bwlink,
      bwopt,
      bwpages,
      bwxguides,
      bwyguides,
    ]
    values = PropertiesEditor.getValues(
      parentwindow, bedwidgets, settings, 'image', self.tr('Image')
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
      self.trim = [values[7], values[8], values[9], values[10]]
      self.filename = values[11]
      self.link = values[13]
      self.opt = values[14]
      self.pagesCMD = values[15]
      self.xguides_names = values[16].split(',')
      self.yguides_names = values[17].split(',')
      self.refresh_xguides()
      self.refresh_yguides()
      return True
    return False


########################################################### Tikz picture
class TikzPicture(Element):
  """Defines a Tikz picture"""

  def __init__(self, *args, **kwargs):
    """Initialisation"""
    super().__init__()
    if len(args) > 0 and type(args[0]) is ET.Element:
      self.readxml(*args, **kwargs)
    else:
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
    pagesCMD='',
    pagesList=(),
    imgs=None,
    hover=0,
    selected=False,
    group=None,
    before='',
    xguides_names=('left', 'center', 'right'),
    yguides_names=('bottom', 'center', 'top'),
    paper_ratio=1,
    current_align_x=(),
    current_align_y=(),
    locked_props=(),
    tikzcmd='',
    origratio=None,
  ):
    """Initialisation from parameters"""
    super().init(
      x,
      y,
      w,
      h,
      minw,
      minh,
      angle_deg,
      pagesCMD,
      pagesList,
      imgs,
      hover,
      selected,
      group,
      before,
      xguides_names,
      yguides_names,
      paper_ratio,
      current_align_x,
      current_align_y,
      locked_props,
    )
    self.tikzcmd = tikzcmd
    # default widht / height ratio
    if origratio:
      self.origratio = origratio
    else:
      self.origratio = w / h
    # Check if the width/height ratio is locked to the default value
    if locked_props is None and self.isOrigratio():
      self.locked_props = ['ratio']

  def readxml(self, xmlElement, npages, slide_imgs, paper_ratio):
    """Initialisation from xml file"""
    super().readxml(xmlElement, npages, slide_imgs, paper_ratio)
    self.tikzcmd = striplines(xmlElement.get('tikzcmd').strip(), 6)
    self.origratio = float(xmlElement.get('origratio'))
    self.locked_props = ['ratio'] if xmlElement.get('isorigratio') == '1' else []
    self.xguides_names = ['left', 'center', 'right']
    self.yguides_names = ['bottom', 'center', 'top']
    self.minw = settings.epsilon
    self.minh = settings.epsilon

  def copy(self):
    """Deep copy function"""
    return TikzPicture(
      self.x,
      self.y,
      self.w,
      self.h,
      self.minw,
      self.minh,
      self.angle_deg,
      self.pagesCMD,
      self.pagesList,
      self.imgs,
      self.hover,
      self.selected,
      self.group,
      self.before,
      self.xguides_names,
      self.yguides_names,
      self.paper_ratio,
      self.current_align_x,
      self.current_align_y,
      self.locked_props,
      self.tikzcmd,
      self.origratio,
    )

  def writeTeX(self, groups):
    """Write the TeX extract from the element properties"""
    # Try and put a correct indenting
    tex = ''
    if self.before.strip():
      tex += spacelines(self.before.strip(), 4) + '\n'
    tex += '    \\tkp{'
    tex += f'{self.x:.4f},{self.y:.4f},{self.w:.4f}'
    if not self.isOrigratio():
      tex += f';height={self.h:.4f}'
    if self.angle_deg != 0:
      tex += f';angle={self.angle_deg:.0f}'
    if self.pagesCMD not in ('', '1-'):
      tex += f';pages={self.pagesCMD}'
    if self.group:
      tex += f';group={groups.index(self.group) + 1}'
    tex += '}{'
    if '\n' in self.tikzcmd.strip():
      tex += '\n' + spacelines(self.tikzcmd.strip(), 6) + '\n    }'
    else:
      tex += self.tikzcmd.strip() + '}'
    return tex

  def isOrigratio(self):
    """Check if the current w/h ratio preserve the original ratio"""
    return abs(self.w - self.h * self.origratio) < settings.epsilon

  def edit(self, parentwindow):
    """Launch the PropertiesEditor (see editor.py) to edit the Image properties."""
    # Initial values of props (before editing)
    init_values = [
      self.x,
      self.y,
      self.w,
      self.h,
      ('ratio' in self.locked_props),
      None,
      self.angle_deg,
      self.tikzcmd,
      self.pagesCMD,
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
    bwtikzcmd = BedAdjustTextEdit(
      init_values[7], label=self.tr('Tikz command'), highlight=True
    )
    bwpages = BedLineEdit(init_values[8], label=self.tr('Pages'))
    bwxguides = BedLineEdit(init_values[9], label=self.tr('x guides'))
    bwyguides = BedLineEdit(init_values[10], label=self.tr('y guides'))
    bedwidgets = [
      bwx,
      bwy,
      bww,
      bwh,
      bwlock,
      bwreset,
      bwangle,
      bwtikzcmd,
      bwpages,
      bwxguides,
      bwyguides,
    ]
    values = PropertiesEditor.getValues(
      parentwindow, bedwidgets, settings, 'tikzpicture', self.tr('Tikz Picture')
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
      self.tikzcmd = values[7]
      self.pagesCMD = values[8]
      self.xguides_names = values[9].split(',')
      self.yguides_names = values[10].split(',')
      self.refresh_xguides()
      self.refresh_yguides()
      return True
    return False


########################################################### ARROW
class Arrow(Element):
  """Defines an arrow"""

  def __init__(self, *args, **kwargs):
    """Initialisation"""
    super().__init__()
    if len(args) > 0 and type(args[0]) is ET.Element:
      self.readxml(*args, **kwargs)
    else:
      self.init(*args, **kwargs)
    self.refresh_xguides()
    self.refresh_yguides()

  def init(
    self,
    x=0,
    y=0,
    w=1,
    h=1,
    minw=0,
    minh=0,
    angle_deg=0,
    pagesCMD='',
    pagesList=(),
    imgs=None,
    hover=0,
    selected=False,
    group=None,
    before='',
    xguides_names=('AC', 'BD'),
    yguides_names=('AC', 'BD'),
    paper_ratio=1,
    current_align_x=(),
    current_align_y=(),
    locked_props=(),
    opt='',
    paper_h=1,
  ):
    """Initialisation from parameters"""
    super().init(
      x,
      y,
      w,
      h,
      minw,
      minh,
      angle_deg,
      pagesCMD,
      pagesList,
      imgs,
      hover,
      selected,
      group,
      before,
      xguides_names,
      yguides_names,
      paper_ratio,
      current_align_x,
      current_align_y,
      locked_props,
    )
    self.opt = opt
    self.paper_h = paper_h

  def readxml(self, xmlElement, npages, slide_imgs, paper_ratio, paper_h):
    """Initialisation from xml file"""
    super().readxml(xmlElement, npages, slide_imgs, paper_ratio)
    self.opt = xmlElement.get('ukoa')
    self.paper_h = paper_h
    self.xguides_names = ['AC', 'BD']
    self.yguides_names = ['AC', 'BD']

  def copy(self):
    """Deep copy function"""
    return Arrow(
      self.x,
      self.y,
      self.w,
      self.h,
      self.minw,
      self.minh,
      self.angle_deg,
      self.pagesCMD,
      self.pagesList,
      self.imgs,
      self.hover,
      self.selected,
      self.group,
      self.before,
      self.xguides_names,
      self.yguides_names,
      self.paper_ratio,
      self.current_align_x,
      self.current_align_y,
      self.locked_props,
      self.opt,
      self.paper_h,
    )

  def writeTeX(self, groups):
    """Write the TeX extract from the element properties"""
    # Try and put a correct indenting
    tex = ''
    if self.before.strip():
      tex += spacelines(self.before.strip(), 4) + '\n'
    tex += '    \\arw{'
    # get x1,x2...
    x1, y1, x2, y2, lw = self.getExtremaFromGeom()
    tex += f'{self.x1:.4f},{self.y1:.4f},{self.x2:.4f},{self.y2:.4f}'
    if self.pagesCMD not in ('', '1-'):
      tex += f';pages={self.pagesCMD}'
    if abs(lw - 1) >= 1e-2:
      tex += f';lw={lw:.2f}'
    if self.opt != '':
      tex += f';{self.opt}'
    if self.group:
      tex += f';group={groups.index(self.group) + 1}'
    tex += '}'
    return tex

  def getExtremaFromGeom(self):
    """Find the position of extrema (x1,...,y2) of the arrow + lw"""
    x1 = self.get_xguide('AC')
    y1 = self.get_yguide('AC')
    x2 = self.get_xguide('BD')
    y2 = self.get_yguide('BD')
    lw = round(self.h * self.paper_h, 2)
    return (x1, y1, x2, y2, lw)

  def setGeomFromExtrema(self, vec):
    """Compute x,y,w,h,angle from x1,..,y2,lw"""
    x1 = vec[0]
    y1 = vec[1]
    x2 = vec[2]
    y2 = vec[3]
    lw = vec[4]
    self.angle_rad = -math.atan2((y2 - y1), (x2 - x1) * self.paper_ratio)
    self.angle_deg = self.angle_rad * 180 / math.pi
    self.w = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2 / self.paper_ratio**2)
    self.h = lw / self.paper_h
    self.x = x1 - math.sin(self.angle_rad) * self.h / self.paper_ratio / 2
    self.y = y1 - math.cos(self.angle_rad) * self.h / 2
    self.refresh_xguides()
    self.refresh_yguides()

  def wheel(self, deltax, deltay):
    """Change line width when mouse scrolling"""
    self.wheely += deltay
    self.wheely = max(self.wheely, -self.h0 * 10 * self.paper_h)
    self.resize_wh(0, self.wheely / 10 / self.paper_h, 'center')

  def selectCursor(self):
    """Choose which cursor should be drawn
    according to the mouse position and keyboard modifiers.
    """
    # Add extrema move possibility to the super function
    # If Shift is pressed  -> classical resizing
    # else allow x1, x2 independent move
    if (not self.shiftmod) and (not self.metamod) and (self.hover % 10 > 0):
      return QtCore.Qt.CrossCursor
    return super().selectCursor()

  def saveGeometry(self):
    """Initialisation before a move/resize/rotate event"""
    # Just remember the initial geometry
    super().saveGeometry()
    self.extrema0 = list(self.getExtremaFromGeom())
    self.extrema = list(self.getExtremaFromGeom())

  def move_x1(self, Dx):
    """Mouse move x1"""
    self.extrema[0] = self.extrema0[0] + Dx
    self.setGeomFromExtrema(self.extrema)
    self.refresh_xguides()

  def move_y1(self, Dy):
    """Mouse move y1"""
    self.extrema[1] = self.extrema0[1] + Dy
    self.setGeomFromExtrema(self.extrema)
    self.refresh_yguides()

  def move_x2(self, Dx):
    """Mouse move x2"""
    self.extrema[2] = self.extrema0[2] + Dx
    self.setGeomFromExtrema(self.extrema)
    self.refresh_xguides()

  def move_y2(self, Dy):
    """Mouse move y2"""
    self.extrema[3] = self.extrema0[3] + Dy
    self.setGeomFromExtrema(self.extrema)
    self.refresh_yguides()

  def magnet_move_x1(self, Dx, dx, extern_xguides):
    """Mouse move x1 and get attracted by guides"""
    if dx != 0:
      tmp = list(self.xguides_names)
      self.xguides_names = ['AC']
      self.move_x1(Dx)
      delta = self.closest_xguide(extern_xguides)
      self.xguides_names = tmp
      if delta * dx >= 0:
        self.move_x1(Dx + delta)

  def magnet_move_y1(self, Dy, dy, extern_yguides):
    """Mouse move y1 and get attracted by guides"""
    if dy != 0:
      tmp = list(self.yguides_names)
      self.yguides_names = ['AC']
      self.move_y1(Dy)
      delta = self.closest_yguide(extern_yguides)
      self.yguides_names = tmp
      if delta * dy >= 0:
        self.move_y1(Dy + delta)

  def magnet_move_x2(self, Dx, dx, extern_xguides):
    """Mouse move x2 and get attracted by guides"""
    if dx != 0:
      tmp = list(self.xguides_names)
      self.xguides_names = ['BD']
      self.move_x2(Dx)
      delta = self.closest_xguide(extern_xguides)
      self.xguides_names = tmp
      if delta * dx >= 0:
        self.move_x2(Dx + delta)

  def magnet_move_y2(self, Dy, dy, extern_yguides):
    """Mouse move y2 and get attracted by guides"""
    if dy != 0:
      tmp = list(self.yguides_names)
      self.yguides_names = ['BD']
      self.move_y2(Dy)
      delta = self.closest_yguide(extern_yguides)
      self.yguides_names = tmp
      if delta * dy >= 0:
        self.move_y2(Dy + delta)

  def magnet_move1(self, Dx, Dy, dx, dy, extern_xguides, extern_yguides):
    """Mouse move x1,y1 and get attracted by guides"""
    self.magnet_move_x1(Dx, dx, extern_xguides)
    self.magnet_move_y1(Dy, dy, extern_yguides)

  def magnet_move2(self, Dx, Dy, dx, dy, extern_xguides, extern_yguides):
    """Mouse move x2,y2 and get attracted by guides"""
    self.magnet_move_x2(Dx, dx, extern_xguides)
    self.magnet_move_y2(Dy, dy, extern_yguides)

  def change_geom(self, Dx, Dy, dx, dy, extern_xguides, extern_yguides):
    """Change the geometry of the element according to mouse move.
    Decide wether to move/move extrema/resize/rotate
    depending on mouse position and key modifiers.
    """
    # Add move extrema possibility to the super function
    if (not self.shiftmod) and (not self.metamod) and (self.hover0 % 10 > 0):
      if self.hover0 % 10 == 1:
        self.magnet_move1(Dx, Dy, dx, dy, extern_xguides, extern_yguides)
      else:
        self.magnet_move2(Dx, Dy, dx, dy, extern_xguides, extern_yguides)
    else:
      super().change_geom(Dx, Dy, dx, dy, extern_xguides, extern_yguides)

  def edit(self, parentwindow):
    """Launch the PropertiesEditor (see editor.py) to edit the Arrow properties."""
    # Initial values of props (before editing)
    init_values = [
      *self.getExtremaFromGeom(),
      self.angle_deg,
      self.opt,
      self.pagesCMD,
      ','.join(self.xguides_names),
      ','.join(self.yguides_names),
    ]

    # Define all the onChange functions (see editor.py)
    def oCxy(parent):
      """Change x1,x2,y1,or y2 -> Update angle,w"""
      parent.changing = True
      x1 = parent.bedwidgets[0].value()
      y1 = parent.bedwidgets[1].value()
      x2 = parent.bedwidgets[2].value()
      y2 = parent.bedwidgets[3].value()
      anglerad = -math.atan2((y2 - y1), (x2 - x1) * self.paper_ratio)
      angledeg = anglerad * 180 / math.pi
      parent.bedwidgets[5].setValue(angledeg)
      parent.changing = False

    def oCangle(parent):
      """Change angle -> Update x2,y2"""
      parent.changing = True
      x1 = parent.bedwidgets[0].value()
      y1 = parent.bedwidgets[1].value()
      x2 = parent.bedwidgets[2].value()
      y2 = parent.bedwidgets[3].value()
      angledeg = parent.bedwidgets[5].value()
      anglerad = angledeg * math.pi / 180
      w = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2 / self.paper_ratio**2)
      parent.bedwidgets[2].setValue(x1 + w * math.cos(anglerad))
      parent.bedwidgets[3].setValue(y1 - w * math.sin(anglerad) * self.paper_ratio)
      parent.changing = False

    # Define BedWidget for each prop (see editor.py)
    bwx1 = BedDoubleSpinBox(init_values[0], -1, 2, 0.01, 4, label='x1', onChange=oCxy)
    bwy1 = BedDoubleSpinBox(init_values[1], -1, 2, 0.01, 4, label='y1', onChange=oCxy)
    bwx2 = BedDoubleSpinBox(init_values[2], -1, 2, 0.01, 4, label='x2', onChange=oCxy)
    bwy2 = BedDoubleSpinBox(init_values[3], -1, 2, 0.01, 4, label='y2', onChange=oCxy)
    bwlw = BedDoubleSpinBox(init_values[4], 0, float('inf'), 1, 2, label='lw')
    bwangle = BedDoubleSpinBox(
      init_values[5], -180, 360, 5, 2, label=self.tr('Angle'), onChange=oCangle
    )
    bwopt = BedLineEdit(init_values[6], label=self.tr('Opt. args.'))
    bwpages = BedLineEdit(init_values[7], label=self.tr('Pages'))
    bwxguides = BedLineEdit(init_values[8], label=self.tr('x guides'))
    bwyguides = BedLineEdit(init_values[9], label=self.tr('y guides'))
    bedwidgets = [
      bwx1,
      bwy1,
      bwx2,
      bwy2,
      bwlw,
      bwangle,
      bwopt,
      bwpages,
      bwxguides,
      bwyguides,
    ]
    values = PropertiesEditor.getValues(
      parentwindow, bedwidgets, settings, 'arrow', self.tr('Arrow')
    )

    # Check if values have changed
    if values:
      # Update properties
      if any(val != initval for val, initval in zip(values[:5], init_values[:5])):
        self.setGeomFromExtrema(values[:5])
      self.opt = values[6]
      self.pagesCMD = values[7]
      self.xguides_names = values[8].split(',')
      self.yguides_names = values[9].split(',')
      self.refresh_xguides()
      self.refresh_yguides()
      return True
    return False

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

# This file defines the Document class (complete LaTeX-Beamer document)

import os

import pymupdf
from PySide6 import QtCore, QtGui

from . import parsing
from .editor import BedAdjustTextEdit, PropertiesEditor
from .frame import Frame
from .helpers import spacelines
from .settings import settings


class Document(QtCore.QObject):
  """Document class represents a complete LaTeX-Beamer document
  It contains a header (LaTeX preamble), Beamer frames, and a footer
  """

  def __init__(
    self,
    header='',
    footer='',
    frames=(),
    paper_w=None,
    paper_h=None,
    npages=None,
    modified=False,
  ):
    """Initialisation"""
    super().__init__()
    self.header = header
    self.footer = footer
    self.frames = []
    # Copy the frames instead of simply linking them
    for f in frames:
      self.frames.append(f.copy())
    self.nframes = len(self.frames)
    self.paper_w = paper_w
    self.paper_h = paper_h
    self.paper_ratio = paper_w / paper_h if (paper_w and paper_h) else None
    self.npages = npages
    self.modified = modified

  def copy(self):
    """Copy function (deep copy)"""
    return Document(
      self.header,
      self.footer,
      self.frames,
      self.paper_w,
      self.paper_h,
      self.npages,
      self.modified,
    )

  def readDoc(self, filename):
    """Read document from pdflatex compilation outputs"""
    imgs = self.loadpdf(filename + '.pdf')
    self.readxml(filename, imgs)

  def loadpdf(self, pdffile):
    """Extract images from the pdf file (output of pdflatex)"""
    pdf = pymupdf.open(pdffile)
    pixs = [page.get_pixmap(dpi=settings.dpi) for page in pdf]
    imgs = [
      QtGui.QImage(
        pix.samples,
        pix.width,
        pix.height,
        QtGui.QImage.Format_RGBA8888 if pix.alpha else QtGui.QImage.Format_RGB888,
      )
      for pix in pixs
    ]
    return imgs

  def readxml(self, filename, imgs):
    """Read the xml tree of the latex document"""
    xml_doc = parsing.parseall(filename)
    self.header = xml_doc.get('header').strip()
    self.footer = xml_doc.get('footer').strip()
    self.nframes = int(xml_doc.get('n_frames'))
    self.npages = int(xml_doc.get('n_pages'))
    self.paper_w = float(xml_doc.get('paper_w'))
    self.paper_h = float(xml_doc.get('paper_h'))
    self.paper_ratio = self.paper_w / self.paper_h
    self.modified = False
    self.frames = []
    for xml_frame in xml_doc:
      self.frames.append(Frame(xml_frame, imgs, self.paper_ratio, self.paper_h))

  def writeTeX(self, texfile, single_frame=-1):
    """Write the Document in a TeX file"""
    # Header
    tex = self.header + '\n'
    # Frames
    for kfr, fr in enumerate(self.frames):
      if single_frame in (-1, kfr):
        tex += fr.writeTeX() + '\n'
      elif fr.before.strip():
        # Put the in-between frames content anyway
        tex += spacelines(fr.before.strip(), 2) + '\n'
    # If compiling single frame, put a dummy frame at the end to capture
    # remaining in-between frames content (sections...)
    if single_frame > -1:
      tex += '\\begin{frame}\\end{frame}\n'
    # Footer
    tex += self.footer + '\n'
    # Writing
    with open(texfile, 'w') as f:
      f.write(tex)
    # Indent the tex file if indent_cmd available
    if settings.indent_cmd != '':
      if '%f' in settings.indent_cmd:
        os.system(settings.indent_cmd.replace('%f', texfile))
      else:
        os.system(settings.indent_cmd + ' ' + texfile)

  def edit(self, parentwindow):
    """Launch the PropertiesEditor (see editor.py) to edit the Document properties."""
    # Initial values of props (before editing)
    init_values = [self.header, self.footer]
    # Define BedWidget for each prop (see editor.py)
    bwheader = BedAdjustTextEdit(
      init_values[0], label=self.tr('Header'), highlight=True
    )
    bwfooter = BedAdjustTextEdit(
      init_values[1], label=self.tr('Footer'), highlight=True
    )
    bedwidgets = [bwheader, bwfooter]
    values = PropertiesEditor.getValues(
      parentwindow, bedwidgets, settings, 'document', self.tr('Document')
    )
    # Check if values have changed
    if values:
      # Update properties
      self.header = values[0]
      self.footer = values[1]
      return True
    return False

  def clean_imgs(self):
    """Clean all preview images from the document's frames."""
    for frame in self.frames:
      frame.clean_imgs()
      frame.clean_imgs()

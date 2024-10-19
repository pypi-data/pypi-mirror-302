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

# This file defines TeX parsing functions

import math
import xml.etree.ElementTree as ET


class MissingBEdLatexPackageError(Exception):
  """Raise this when \\usepackage{bed} is missing in the TeX file preamble."""

  def __init__(self):
    super().__init__('Could not find \\usepackage{bed} in TeX file preamble.')


# Generic parsing functions
def _aux_find(string, substring, escape=None):
  """Find the first occurence of a substring (can be a list of possible substrings)
  in a string and return its position (start,end).
  Do not count the occurences preceded by the escape string.
  """
  subs = substring
  if type(subs) is str:
    subs = [subs]
  lsubs = [(len(sub), sub) for sub in subs]
  if escape:
    lesc = len(escape)
  k = 0
  while k < len(string):
    for lsub, sub in lsubs:
      if string[k : k + lsub] == sub:
        return (k, k + lsub)
    if escape and string[k : k + lesc] == escape:
      k += lesc + 1
    else:
      k += 1
  return (-1, -1)


def _aux_findall(string, substring, escape=None):
  """Find all occurences of a substring (can be a list of possible substrings)
  in a string and return their position (list of (start,end)).
  Do not count the occurences preceded by the escape string.
  """
  inds = []
  k = 0
  while k < len(string):
    s, e = _aux_find(string[k:], substring, escape)
    if s < 0:
      break
    inds.append((k + s, k + e))
    k += e
  return inds


def find(string, substring, escape=None, se='start', restrict=None):
  """Find the first occurence of a substring in a string restricted
  to the interval list restrict.
  se="start" -> output only the start position of the substring
  se="end" -> output only the end position of the substring
  otherwise -> output start,end position of the substring
  """
  if not restrict:
    restrict = [[0, len(string)]]
  for a, b in restrict:
    s, e = _aux_find(string[a:b], substring, escape)
    if s >= 0:
      if se == 'start':
        return a + s
      if se == 'end':
        return a + e
      return (a + s, a + e)
  if se in ('start', 'end'):
    return -1
  return (-1, -1)


def findall(string, substring, escape=None, se='start', restrict=None):
  """Find all the occurences of a substring in a string restricted
  to the interval list restrict.
  se="start" -> output only the start position of the substring
  se="end" -> output only the end position of the substring
  otherwise -> output start,end position of the substring
  """
  if not restrict:
    restrict = [[0, len(string)]]
  inds = []
  for a, b in restrict:
    tmp = _aux_findall(string[a:b], substring, escape)
    for s, e in tmp:
      if se == 'start':
        inds.append(a + s)
      elif se == 'end':
        inds.append(a + e)
      else:
        inds.append((a + s, a + e))
  return inds


def match(lstart, lend, start, multilevel=True):
  """Find the ending substring matching the starting substring
  lstart: list of positions of start substrings
  lend: list of positions of end substrings
  start: position of the start substring we want to match
  """
  kstart = 0
  while kstart < len(lstart) and lstart[kstart] < start:
    kstart += 1
  kend = 0
  while kend < len(lend) and lend[kend] <= lstart[kstart]:
    kend += 1
  if multilevel:
    ks = kstart + 1
    ke = kend
    while ke < len(lend) and ke - kend < ks - kstart:
      while ks < len(lstart) and lstart[ks] < lend[ke]:
        ks += 1
      ke += 1
    if ke - kend < ks - kstart:
      return -1
    return lend[ke - 1]
  return lend[kend] if kend < len(lend) else -1


def find_comments(string, start='%', end='\n', escape_start='\\', escape_end=None):
  """Find all the comments in the file.
  Comments are delimited by the start and end substrings
  except when preceded by escape substrings.
  """
  comstart = findall(string, start, escape_start)
  comend = findall(string, end, escape_end, 'end')
  comments = []
  k = 0
  e = 0
  while k < len(comstart):
    if comstart[k] >= e:
      s = comstart[k]
      if comstart[k] == e:
        s = comments[-1][0]
        del comments[-1]
      e = match(comstart[k:], comend, comstart[k], False)
      if e < 0:
        break
      comments.append((s, e))
    k += 1
  return comments


def find_strings(string, delimitor='"', escape='\\', restrict=None):
  """Find all the strings (begin and end delimitor are the same)"""
  ldel = len(delimitor)
  dels = findall(string, delimitor, escape, restrict=restrict)
  if len(dels) % 2 == 1:
    return -1
  strs = []
  for s, e in zip(dels[::2], dels[1::2]):
    strs.append((s, e + ldel))
  return strs


def complementary(intlist, n):
  """Compute the complementary set of interval"""
  oldb = 0
  comp = []
  for a, b in intlist:
    if a > oldb:
      comp.append((oldb, a))
    oldb = b
  if oldb < n:
    comp.append((oldb, n))
  return comp


def intersection(intlist1, intlist2):
  """Compute the intersection between 2 intervals"""
  inter = []
  for a1, b1 in intlist1:
    for a2, b2 in intlist2:
      ia = max(a1, a2)
      ib = min(b1, b2)
      if ia < ib:
        inter.append((ia, ib))
  return inter


################################# Initial parsing of the tex file
def parsetex(jobname, xml_doc):
  """Parse the whole tex file to find frames, elements...
  and construct xml tree of it.
  """
  with open(jobname + '.tex') as f:
    tex = f.read()
  ltex = len(tex)

  # Find commented parts in the file
  coms = find_comments(tex)
  # Take the complementary to find the non-commented parts
  code = complementary(coms, ltex)

  if find(tex, '\\usepackage{bed}', escape='\\', restrict=code, se='start') == -1:
    raise MissingBEdLatexPackageError
  # Find the {document} (begin, end)
  doc_b = find(tex, '\\begin{document}', escape='\\', restrict=code, se='end')
  doc_e = find(tex, '\\end{document}', escape='\\', restrict=code)
  xml_doc.set('header', tex[:doc_b])
  # Find the non-commented parts of the code inside the {document}
  doc_code = intersection(code, [[doc_b, doc_e]])
  # Find the frames (begin, end)
  frames_b = findall(tex, '\\begin{frame}', escape='\\', restrict=doc_code, se='both')
  frames_e = findall(tex, '\\end{frame}', escape='\\', restrict=doc_code, se='both')
  # Explore each Frame
  pfr_e = doc_b
  for (fr_bb, fr_be), (fr_eb, fr_ee) in zip(frames_b, frames_e):
    # Add new frame in the tree
    xml_fr = ET.SubElement(xml_doc, 'frame')
    # Initialisation
    xml_fr.set('n_pages', '1')
    xml_fr.set('n_groups', '0')
    # Code that appear before the frame
    xml_fr.set('before', tex[pfr_e:fr_bb])
    pfr_e = fr_ee
    # Code inside frame
    frame_code = intersection(doc_code, [[fr_be, fr_eb]])
    # Find all the brackets in the frame
    brackets_b = findall(tex, '{', escape='\\', restrict=frame_code)
    brackets_e = findall(tex, '}', escape='\\', restrict=frame_code, se='end')
    # Find all the elements (\txt, \img, \tkp, \arw)
    elems = findall(
      tex,
      ['\\txt', '\\img', '\\tkp', '\\arw'],
      escape='\\',
      restrict=frame_code,
      se='both',
    )
    pel_e = -1
    # Analyse each element
    for el_b, el_e in elems:
      # Create new element
      xml_el = ET.SubElement(xml_fr, tex[el_b + 1 : el_e])
      if pel_e == -1:
        # Find frame title if first element
        xml_fr.set('title', tex[fr_be:el_b])
        xml_el.set('before', '')
      else:
        # Code before element
        xml_el.set('before', tex[pel_e:el_b])
      if tex[el_b:el_e] == '\\arw':
        pel_e = match(brackets_b, brackets_e, el_e)
      else:
        firstb_e = match(brackets_b, brackets_e, el_e)
        pel_e = match(brackets_b, brackets_e, firstb_e)
        if tex[el_b:el_e] == '\\txt':
          xml_el.set('text', tex[firstb_e + 1 : pel_e - 1])
        elif tex[el_b:el_e] == '\\img':
          xml_el.set('name', tex[firstb_e + 1 : pel_e - 1])
        else:
          xml_el.set('tikzcmd', tex[firstb_e + 1 : pel_e - 1])

    # Find title if no elements
    if not elems:
      xml_fr.set('title', tex[fr_be:fr_eb])
      pel_e = fr_eb
    xml_fr.set('footer', tex[pel_e:fr_eb])
  xml_doc.set('footer', tex[fr_ee:])
  xml_doc.set('n_frames', str(len(frames_b)))


def parselog(jobname, xml_doc):
  """Parsing of the log file (after Tex compilation)
  The bed latex package (see ../latex/bed.sty) output some informations to the log file
  """
  # Read all lines in the log
  with open(jobname + '.log', encoding='ISO-8859-1') as f:
    log = f.readlines()
  k = 0
  frame = -1
  framefirstpage = 0
  nelem = 0
  while k < len(log):
    # Check if this is an interesting line (must start with BEd package)
    if log[k][:11] == 'BEd package':
      # Initial informations (paper size)
      if log[k][14:17] == 'beg':
        xml_doc.set('paper_w', log[k + 1].strip()[:-2])
        xml_doc.set('paper_h', log[k + 2].strip()[:-2])
        paperw = float(log[k + 1].strip()[:-2])
        paperh = float(log[k + 2].strip()[:-2])
        paperratio = paperw / paperh
        k += 2
      # Final informations (total number of pages)
      elif log[k][14:17] == 'end':
        xml_doc.set('n_pages', str(int(log[k + 1]) - 1))
        if frame > -1:
          xml_doc[frame].set('n_pages', str(int(log[k + 1]) - framefirstpage))
          xml_doc[frame].set('n_elements', str(nelem))
        k += 1
      elif log[k][14:17] == 'fra':
        # Get frame / firstpage where it appears
        if frame > -1:
          xml_doc[frame].set('n_pages', str(int(log[k + 2]) - framefirstpage))
          xml_doc[frame].set('n_elements', str(nelem))
        frame = int(log[k + 1])
        framefirstpage = int(log[k + 2])
        nelem = 0
        xml_doc[frame].set('first_page', str(framefirstpage))
        xml_doc[frame].set('n_pages', '1')
        k += 2
      else:
        # Element information
        page = int(log[k + 2])
        if page == framefirstpage:
          # Check type of element
          if log[k][14:17] == 'txt':
            # Text
            xml_doc[frame][nelem].set('x', log[k + 3].strip())
            xml_doc[frame][nelem].set('y', log[k + 4].strip())
            xml_doc[frame][nelem].set('w', log[k + 5].strip())
            xml_doc[frame][nelem].set('h', log[k + 6].strip())
            xml_doc[frame][nelem].set('minh', log[k + 7].strip())
            xml_doc[frame][nelem].set('angle', log[k + 8].strip())
            xml_doc[frame][nelem].set('pages', log[k + 9].strip())
            xml_doc[frame][nelem].set('group', log[k + 10].strip())
            xml_doc[frame][nelem].set('align', log[k + 11].strip())
            k += 11
          elif log[k][14:17] == 'img':
            # Image
            xml_doc[frame][nelem].set('x', log[k + 3].strip())
            xml_doc[frame][nelem].set('y', log[k + 4].strip())
            xml_doc[frame][nelem].set('w', log[k + 5].strip())
            xml_doc[frame][nelem].set('h', log[k + 6].strip())
            xml_doc[frame][nelem].set('angle', log[k + 7].strip())
            xml_doc[frame][nelem].set('pages', log[k + 8].strip())
            xml_doc[frame][nelem].set('group', log[k + 9].strip())
            xml_doc[frame][nelem].set('trim', log[k + 10].strip())
            xml_doc[frame][nelem].set('link', log[k + 11].strip())
            xml_doc[frame][nelem].set('origratio', log[k + 12].strip())
            xml_doc[frame][nelem].set(
              'isorigratio', ('1' if log[k + 13].strip() == '-1' else '0')
            )
            xml_doc[frame][nelem].set('ukoa', log[k + 14].strip()[1:])
            k += 14
          elif log[k][14:17] == 'tkp':
            # Image
            xml_doc[frame][nelem].set('x', log[k + 3].strip())
            xml_doc[frame][nelem].set('y', log[k + 4].strip())
            xml_doc[frame][nelem].set('w', log[k + 5].strip())
            xml_doc[frame][nelem].set('h', log[k + 6].strip())
            xml_doc[frame][nelem].set('angle', log[k + 7].strip())
            xml_doc[frame][nelem].set('pages', log[k + 8].strip())
            xml_doc[frame][nelem].set('group', log[k + 9].strip())
            xml_doc[frame][nelem].set('origratio', log[k + 10].strip())
            xml_doc[frame][nelem].set(
              'isorigratio', ('1' if log[k + 11].strip() == '-1' else '0')
            )
            k += 11
          elif log[k][14:17] == 'arw':
            # Arrow
            xml_doc[frame][nelem].set('x1', log[k + 3].strip())
            xml_doc[frame][nelem].set('y1', log[k + 4].strip())
            xml_doc[frame][nelem].set('x2', log[k + 5].strip())
            xml_doc[frame][nelem].set('y2', log[k + 6].strip())
            xml_doc[frame][nelem].set('pages', log[k + 7].strip())
            xml_doc[frame][nelem].set('group', log[k + 8].strip())
            xml_doc[frame][nelem].set('lw', log[k + 9].strip())
            xml_doc[frame][nelem].set('ukoa', log[k + 10].strip()[1:])
            x1 = float(log[k + 3])
            y1 = float(log[k + 4])
            x2 = float(log[k + 5])
            y2 = float(log[k + 6])
            lw = float(log[k + 9])
            anglerad = -math.atan2((y2 - y1), (x2 - x1) * paperratio)
            angle = anglerad * 180 / math.pi
            w = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2 / paperratio**2)
            h = lw / paperh
            x = x1 - math.sin(anglerad) * h / paperratio / 2
            y = y1 - math.cos(anglerad) * h / 2
            xml_doc[frame][nelem].set('x', f'{x:.10f}')
            xml_doc[frame][nelem].set('y', f'{y:.10f}')
            xml_doc[frame][nelem].set('w', f'{w:.10f}')
            xml_doc[frame][nelem].set('h', f'{h:.10f}')
            xml_doc[frame][nelem].set('angle', f'{angle:.10f}')
            k += 10
          # Check if the element is in a group
          if xml_doc[frame][nelem].get('group') != '0':
            igroup = int(xml_doc[frame][nelem].get('group'))
            ngroups = max(int(xml_doc[frame].get('n_groups')), igroup)
            xml_doc[frame].set('n_groups', str(ngroups))
          nelem += 1
    k += 1


################################# Final parsing
def endparse(xml_doc):
  nframes = int(xml_doc.get('n_frames'))
  page = int(xml_doc.get('n_pages'))
  for k in range(nframes):
    if not xml_doc[k].get('first_page'):
      if k == 0:
        xml_doc[k].set('first_page', '1')
      else:
        xml_doc[k].set(
          'first_page',
          str(
            int(xml_doc[k - 1].get('first_page')) + int(xml_doc[k - 1].get('n_pages'))
          ),
        )
      if k + 1 == nframes:
        xml_doc[k].set('n_pages', str(page + 1 - int(xml_doc[k].get('first_page'))))
      elif xml_doc[k + 1].get('first_page'):
        xml_doc[k].set(
          'n_pages',
          str(
            int(xml_doc[k + 1].get('first_page')) - int(xml_doc[k].get('first_page'))
          ),
        )
      else:
        xml_doc[k].set('n_pages', '1')
      xml_doc[k].set('n_elements', '0')


def parseall(jobname):
  """Parse tex + log of a document to construct the xml tree"""
  # Create root element of xml tree
  xml_doc = ET.Element('document')
  # Parse tex
  parsetex(jobname, xml_doc)
  # Parse log
  parselog(jobname, xml_doc)
  # Finalize the xml tree
  endparse(xml_doc)
  return xml_doc

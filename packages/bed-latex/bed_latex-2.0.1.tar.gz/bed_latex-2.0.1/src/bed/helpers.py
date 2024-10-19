# Useful functions:
def stripmax(string, k=0):
  """Function similar to str.strip() but with a maximum number of removed
  spaces on the left (k).
  """
  if k == 0:
    # Usual strip()
    return string.strip()
  # Do not remove more that k spaces on the left
  st = string
  for _ in range(min(k, len(string))):
    if st[0].isspace():
      st = st[1:]
    else:
      break
  # Usual strip on the right
  return st.rstrip()


def striplines(string, k=0):
  """Strip each line using stripmax"""
  return '\n'.join([stripmax(line, k) for line in string.split('\n')])


def spacelines(string, k=0):
  """Add k spaces in front of each line"""
  spaces = k * ' '
  return spaces + ('\n' + spaces).join(string.split('\n'))


def argmin(values):
  """Index of minimum"""
  return values.index(min(values))


def argmax(values):
  """Index of maximum"""
  return values.index(max(values))

# ultralight dictionary database
# Ben Southgate (bsouthga@gmail.com)
# 10/24/14
# license : MIT
import itertools

def match(tree, query):
  '''
    return boolean indicating if all
    elements of query match tree
  '''
  for k in query:
    v = query[k]
    if k not in tree:
      return False
    if type(v) == dict:
      if not match(tree[k], v):
        return False 
    else:
      if hasattr(v, '__call__'):
        result = v(tree[k])
        if type(result) == bool:
          if not result:
            return False 
        else:
          e = 'matching function for {} must return boolean.'.format(k)
          raise Exception(e)
      elif not v == tree[k]:
          return False 
  return True

class DDB(object):

  def __init__(self, data):
    self.d = data

  def __repr__(self):
    view = list(self.d)
    self.d = (x for x in view)
    return str(view)

  def __iter__(self):
    for item in self.d: yield item

  def __len__(self):
    view = list(self.d)
    self.d = (x for x in view)
    return len(view)

  def split(self):
    view, copy = itertools.tee(self.d)
    self.d = view
    return copy

  def select(self, query):
    return DDB(x for x in self.split() if match(x, query))

  def map(self, transform):
    return DDB(transform(x) for x in self.split())

  def insert(self, item):
    if type(item) == dict or not hasattr(item, '__iter__'):
      item = [item]
    return DDB(x for x in itertools.chain(self.split(), item))

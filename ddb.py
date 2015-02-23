#
# ultralight dictionary database
# Ben Southgate (bsouthga@gmail.com)
# 10/24/14
# license : MIT
#

import itertools


def match(tree, query):
  '''
    return boolean indicating if all
    elements of query match tree

    @param tree : current record being scanned
    @param query : the query to be executed on the data
  '''
  # loop through keys in query
  for k in query:
    # store value for current key
    v = query[k]
    # check if the current query key exists in the data
    if k not in tree:
      return False
    # if the value for this key is itself a dictionary,
    # recurse deeper into the query
    if type(v) == dict:
      if not match(tree[k], v):
        return False
    else:
      # if the value is a function, call the function
      # on the corresponding value in the data
      if hasattr(v, '__call__'):
        result = v(tree[k])
        # necessitate that the function returns a boolean
        if type(result) == bool:
          if not result:
            return False
        else:
          e = 'matching function for {} must return boolean.'.format(k)
          raise Exception(e)
      # if the value simply doesn't equal the data,
      # no match found
      elif not v == tree[k]:
          return False
  return True



class DDB(object):

  def __init__(self, data):
    self.d = data

  def __repr__(self):
    return str(self.to_list())

  def __iter__(self):
    for item in self.d: yield item

  def __len__(self):
    return len(self.to_list())

  def __eq__(self, other):
    return self.to_list() == other

  def to_list(self):
    view = list(self.d)
    self.d = (x for x in view)
    return view

  def split(self):
    view, copy = itertools.tee(self.d)
    self.d = view
    return copy

  def select(self, query=None):
    if query == None:
      return DDB(self.split())
    return DDB(x for x in self.split() if match(x, query))

  def map(self, transform):
    return DDB(transform(x) for x in self.split())

  def insert(self, item):
    if type(item) == dict or not hasattr(item, '__iter__'):
      item = [item]
    self.d = itertools.chain(self.split(), item)
    return self



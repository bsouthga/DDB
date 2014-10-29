# ultralight dictionary database
# Ben Southgate (bsouthga@gmail.com)
# 10/24/14
# license : MIT

def match(tree, query):
  '''
    return boolean indicating if all
    elements of query match tree
  '''
  for k, v in query.items():
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

  def __init__(self, dict_list):
    self.store = dict_list

  def __repr__(self):
    return str(self.store)

  def __iter__(self):
    for item in self.store: yield item

  def __len__(self):
    return len(self.store)

  def __getitem__(self, index):
    return self.store[index]

  def select(self, query):
    return DDB([i for i in self.store if match(i, query)])

  def map(self, transform):
    return DDB([transform(i) for i in self.store])

  def insert(self, item):
    if type(item) == list:
      self.store += item
    else:
      self.store.append(item)
    return self

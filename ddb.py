#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# ultralight dictionary database
# Ben Southgate
# 10/24/14
# license : MIT
#


__author__ = "Ben Southgate <bsouthga@gmail.com>"
__version__ = "0.1"


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
    self.selection = self.store
    self.query = None

  def __repr__(self):
    return str(self.selection)

  def __iter__(self):
    for item in self.selection: 
      yield item

  def __len__(self):
    return len(self.selection)

  def __getitem__(self, index):
    return self.selection[index]

  def select(self, query=None):
    if query in (None, {}):
      query = None 
    self.query = query
    if query == None:
      self.selection = self.store
    else:
      self.selection = [i for i in self.store if match(i, query)]
    return self

  def insert(self, item):
    if type(item) == list:
      self.store += item
      if self.query != None:
        self.selection += [i for i in item if match(i, self.query)]
    else:
      self.store.append(item)
      if match(item, self.query):
        self.selection.append(item)
    return self

from ddb import DDB

test_data = [
  {"a" : 1, "b" : {"x" : 2}}, 
  {"a" : 2, "b" : {"x" : 2}},
  {"a" : 2, "b" : {"x" : 3}}
]

db = DDB(test_data)

selection = db.select({"a" : 2})

print(selection)

print(selection.select({"b" : {"x" : 2}}))

print(selection.insert({"a" : 2}))

print(selection.select({"b" : {"x" : lambda x : x < 3}}))

for item in selection:
  print(item)

import random

def addFuzzyAsquared(item):
  item['a_sq'] = item['a']**2 + random.randint(0, 20)
  return item

print(selection.map(addFuzzyAsquared).select({"a_sq" : lambda x : x < 10}))
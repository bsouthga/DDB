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
for item in db:
  print(item)
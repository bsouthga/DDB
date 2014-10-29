# [D]ictionary [D]ata [B]ase

A small class for filtering lists of dictionaries in 80 lines of Python

## Usage

Create a database...

```python
from ddb import DDB

test_data = [
  {"a" : 1, "b" : {"x" : 2}}, 
  {"a" : 2, "b" : {"x" : 2}},
  {"a" : 2, "b" : {"x" : 3}}
]

db = DDB(test_data)
```

Filter the database, `db.select()` returns the database for method chaining / new selections

```python
selection = db.select({"a" : 2})
print(selection)
# => [{"a" : 2, "b" : {"x" : 2}}, {"a" : 2, "b" : {"x" : 3}}]
print(selection.select({"b" : {"x" : 2}}))
# Note : DOESNT return a further sub-selection of previous selection
# => [{'a': 1, 'b': {'x': 2}}, {'a': 2, 'b': {'x': 2}}]

```

Insert stuff (it doesn't even have to be the same shape!), 
and have the selection automatically update!

```python
print(selection.insert({"a" : 2}))
# => [{"a" : 2, "b" : {"x" : 2}}, {"a" : 2, "b" : {"x" : 3}}, {"a" : 2}]

```

Select using functions!


```python
selection = db.select({"b" : {"x" : lambda x : x < 3}})
print(selection)
# => [{'a': 1, 'b': {'x': 2}}, {'a': 2, 'b': {'x': 2}}]

```

Iterate through the selection!

```python
for item in selection:
  print(item)
# =>
#   {'a': 1, 'b': {'x': 2}}
#   {'a': 2, 'b': {'x': 2}}
```

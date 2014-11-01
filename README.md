# [D]ictionary "[D]ata[B]ase"

A class for lazily filtering and manipulating lists of dictionaries in less than 60 lines of Python. Everything is passed as generators, so memory efficiency should be pretty good! There are no dependencies other then the built-in `itertools`.

## Usage

Create a "database"...

```python
from ddb import DDB

test_data = [
  {"a" : 1, "b" : {"x" : 2}}, 
  {"a" : 2, "b" : {"x" : 2}},
  {"a" : 2, "b" : {"x" : 3}}
]

db = DDB(test_data)
```

Filter the "database" using `db.select()`, which returns 
a new DDB with the selection for method chaining / new selections

```python
selection = db.select({"a" : 2})
print(selection)
# => [{"a" : 2, "b" : {"x" : 2}}, {"a" : 2, "b" : {"x" : 3}}]
print(selection.select({"b" : {"x" : 2}}))
# => [{'a': 2, 'b': {'x': 2}}]

```

Insert stuff 

```python
print(selection.insert({"a" : 2}))
# => [{'a': 2, 'b': {'x': 2}}, {'a': 2, 'b': {'x': 3}}, {'a': 2}]

```

Select using functions!


```python
print(selection.select({"b" : {"x" : lambda x : x < 3}}))
# => [{'a': 2, 'b': {'x': 2}}]
```

Iterate through the selection!

```python
for item in selection:
  print(item)
# =>
#  {'a': 2, 'b': {'x': 2}}
#  {'a': 2, 'b': {'x': 3}}
#  {'a': 2}
```

Apply transforms, and chain operations!

```python
import random

def addFuzzyAsquared(item):
  item['a_sq'] = item['a']**2 + random.randint(0, 20)
  return item

print(selection.map(addFuzzyAsquared).select({"a_sq" : lambda x : x < 10}))

```

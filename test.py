#!/usr/bin/python

#
# Basic DDB unit testing
# @bsouthga
# 02/22/15
#



from ddb import DDB
import unittest

class TestDDB(unittest.TestCase):


    def setUp(self):
        # load example data into a test DDB instance
        test_data = [
          {"a" : 1, "b" : {"x" : 2, "y" : {"y_1" : True, "y_2": True}}},
          {"a" : 2, "b" : {"x" : 2, "y" : {"y_1" : True}}},
          {"a" : 2, "b" : {"x" : 3}},
          {"a" : 3}
        ]
        self.db = DDB(test_data)


    def test_selection(self):
      # test basic feature selection
      selection = self.db.select({"b" : {"x" : 3}})
      # equality test
      self.assertEqual(selection, [{"a" : 2, "b" : {"x" : 3}}])


    def test_null_select(self):
      # null selection should return copy
      self.assertEqual(self.db, self.db.select())


    def test_print(self):
        # test basic feature selection
        selection = self.db.select({'a' : 3})
        # string conversion test
        self.assertEqual(str(selection), "[{'a': 3}]")


    def test_iteration(self):
        # test basic feature selection
        selection = self.db.select({'a' : 2})
        # results
        results = [e for e in selection]
        # check list comprehension results
        self.assertEqual(results, [
          {'a': 2, 'b': {'x': 2, 'y': {'y_1': True}}},
          {'a': 2, 'b': {'x': 3}}
        ])
        # check that the iterator has not been consumed
        self.assertEqual(len(results), 2)


    def test_mapping(self):
      # function to map
      def addAsquared(item):
        item['a_sq'] = item['a']**2
        return item
      # map function and select results
      results = self.db.map(addAsquared) \
                       .select({"a_sq" : lambda x : x > 5})
      # check that correct selection was returned,
      # with value added by mapping
      self.assertEqual(results, [{"a": 3, "a_sq" : 9}])


    def test_insert(self):
      # item to add in database
      new_item = {"a" : 2}
      # select subset
      selection = self.db.select({"a" : 3})
      # insert item
      selection.insert(new_item)
      # check successful insertion
      self.assertEqual(selection, [{"a" : 3}, {"a" : 2}])


if __name__ == '__main__':
    unittest.main()
#!/usr/bin/env python
from pqdict import PQDict as pqd
from itertools import combinations
import random
import unittest

def generateData(pkey_type, num_items=None):
    # shuffled set of two-letter dictionary keys
    pairs = combinations('ABCDEFGHIJKLMNOP', 2)
    dkeys = [''.join(pair) for pair in pairs]
    random.shuffle(dkeys)
    if num_items is not None:
        dkeys = dkeys[:num_items]
    else:
        num_items = len(dkeys)
        
    # different sets of priority keys
    if pkey_type == 'int':
        pkeys = [random.randint(0,100) for i in range(num_items)]
    elif pkey_type == 'float':
        pkeys = [random.random() for i in range(num_items)]
    elif pkey_type == 'unique':
        pkeys = list(range(num_items))
        random.shuffle(pkeys) 
    return list(zip(dkeys, pkeys))


class TestPQDict(unittest.TestCase):
    def check_heap_invariant(self, pq):
        heap = pq.heap
        for pos, entry in enumerate(heap):
            if pos: # pos 0 has no parent
                parentpos = (pos-1) >> 1
                self.assertLessEqual(heap[parentpos].pkey, entry.pkey)

    def check_index(self, pq):
        # All heap entries are pointed to by the index (nodefinder)
        n = len(pq.heap)
        nodes = pq.nodefinder.values()
        self.assertEqual(list(range(n)), sorted(nodes))
        # All heap entries map back to the correct dictionary key
        for dkey in pq.nodefinder:
            entry = pq.heap[pq.nodefinder[dkey]]
            self.assertEqual(dkey, entry.dkey)

class TestAPI(TestPQDict):
    def setUp(self):
        self.dkeys = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
        self.pkeys = [5, 8, 7, 3, 9, 12, 1]
        self.items = list(zip(self.dkeys, self.pkeys))

    def test_constructor(self):
        # sequence of pairs
        pq0 = pqd([('A',5), ('B',8), ('C',7), ('D',3), ('E',9), ('F',12), ('G',1)])
        pq1 = pqd(zip(['A', 'B', 'C', 'D', 'E', 'F', 'G'], [5, 8, 7, 3, 9, 12, 1]))
        # dictionary
        pq2 = pqd({'A':5, 'B':8, 'C':7, 'D':3, 'E':9, 'F':12, 'G':1})
        # keyword arguments
        pq3 = pqd(A=5, B=8, C=7, D=3, E=9, F=12, G=1)
        self.assertTrue(pq0==pq1==pq2==pq3)

    def test_equality(self):
        # eq, ne
        pq1 = pqd(self.items)
        pq2 = pqd(self.items)
        self.assertTrue(pq1 == pq2)
        self.assertFalse(pq1 != pq2)

        pq2[random.choice(self.dkeys)] += 1
        self.assertTrue(pq1 != pq2)
        self.assertFalse(pq1 == pq2)

        # pqd == regular dict should be legal and True if they have same key/value pairs
        adict = dict(self.items)
        self.assertEqual(pq1, adict)

        # False for seq of dkeys though
        self.assertNotEqual(pq1, self.dkeys)

    def test_inequalities(self):
        pass

    def test_len(self):
        pq = pqd()
        self.assertEqual(len(pq), 0)
        pq = pqd(self.items)
        self.assertEqual(len(pq), len(self.items))

    def test_contains(self):
        pq = pqd(self.items)
        for dkey in self.dkeys:
            self.assertIn(dkey, pq)

    def test_getitem(self):
        pq = pqd(self.items)
        for dkey, pkey in self.items:
            self.assertEqual(pq[dkey], pkey)

    def test_setitem(self):
        pq = pqd(self.items)
        pq['new'] = 1.0 #add
        self.assertEqual(pq['new'], 1.0)
        pq['new'] = 10.0 #update
        self.assertEqual(pq['new'], 10.0)  

    def test_delitem(self):
        pq = pqd(self.items)
        dkey = random.choice(self.dkeys)
        del pq[dkey]
        self.assertNotIn(dkey, pq)
        self.assertRaises(KeyError, pq.pop, dkey)

    def test_iter(self):
        pq = pqd(self.items)
        for val in iter(pq):
            self.assertIn(val, self.dkeys)
        self.assertEqual(len(list(iter(pq))), len(self.dkeys))

    def test_copy(self):
        pq1 = pqd(self.items)
        pq2 = pq1.copy()
        # equality by value
        self.assertEqual(pq1, pq2)

        dkey = random.choice(self.dkeys)
        pq2[dkey] += 1  
        self.assertNotEqual(pq1[dkey], pq2[dkey])
        self.assertNotEqual(pq1, pq2)

    def test_additem(self):
        pq = pqd(self.items)
        pq.additem('new', 8.0)
        self.assertEqual(pq['new'], 8.0)
        self.assertRaises(KeyError, pq.additem, 'new', 1.5)

    def test_updateitem(self):
        pq = pqd(self.items)
        dkey, pkey = random.choice(self.items)
        # assign same value
        pq.updateitem(dkey, pkey)
        self.assertEqual(pq[dkey], pkey)
        # assign new value
        pq.updateitem(dkey, pkey + 1.0)
        self.assertEqual(pq[dkey], pkey + 1.0)
        # can only update existing dkeys
        self.assertRaises(KeyError, pq.updateitem, 'does_not_exist', 99.0)     

    def test_popitem(self):
        pq = pqd(A=5, B=8, C=1)
        # pop top item
        dkey, pkey = pq.popitem()
        self.assertEqual(dkey,'C') and self.assertEqual(pkey,1)

    def test_pop(self):
        # pop selected item - return pkey
        pq = pqd(A=5, B=8, C=1)
        pkey = pq.pop('B')
        self.assertEqual(pkey, 8)
        pq.pop('A')
        pq.pop('C')
        self.assertRaises(KeyError, pq.pop, 'A')
        self.assertRaises(KeyError, pq.pop, 'does_not_exist')
        self.assertRaises(KeyError, pq.popitem) #pq is now empty

    def test_peek(self):
        # empty
        pq = pqd()
        self.assertRaises(KeyError, pq.peek)
        # non-empty
        for num_items in range(1,30):
            items = generateData('float', num_items)
            pq = pqd(items)
            self.assertTrue(pq.peek() == min(items, key=lambda x: x[1]))


    # inherited methods
    def test_get(self):
        pq = pqd(self.items)
        self.assertEqual(pq.get('A'), 5)
        self.assertEqual(pq.get('A', None), 5)
        self.assertIs(pq.get('does_not_exist', None), None)
        self.assertRaises(KeyError, pq.get('does_not_exist'))

    def test_clear(self):
        pq = pqd(self.items)
        pq.clear()
        self.assertEqual(len(pq), 0)
        self.check_index(pq)

    def test_setdefault(self):
        pq = pqd(self.items)
        self.assertEqual(pq.setdefault('A',99), 5)
        self.assertEqual(pq.setdefault('new',99), 99)
        self.assertEqual(pq['new'], 99)

    def test_update(self):
        pq1 = pqd(self.items)
        pq2 = pqd()
        pq2['C'] = 3000
        pq2['D'] = 4000
        pq2['XYZ'] = 9000
        pq1.update(pq2)
        self.assertEqual(pq1['C'],3000) and \
        self.assertEqual(pq1['D'],4000) and \
        self.assertIn('XYZ',pq1) and \
        self.assertEqual(pq1['XYZ'],9000)

    def test_keys(self):
        # the "keys" are dictionary keys
        pq = pqd(self.items)
        self.assertEqual(sorted(self.dkeys), sorted(pq.keys()))

    def test_values(self):
        # the "values" are priority keys
        pq = pqd(self.items)   
        self.assertEqual(sorted(self.pkeys), sorted(pq.values()))

    def test_items(self):
        pq = pqd(self.items)
        self.assertEqual(sorted(self.items), sorted(pq.items()))


class TestOperations(TestPQDict):
    def test_uncomparable(self):
        # non-comparable priority keys (Python 3 only) 
        # Python 3 has stricter comparison than Python 2
        pq = pqd()
        pq.additem('a',[])
        self.assertRaises(TypeError, pq.additem, 'b', 5)

    def test_heapify(self):
        for size in range(30):
            items = generateData('int', size)
            pq = pqd(items)
            self.check_heap_invariant(pq)
            self.assertTrue(len(pq.heap)==size)
            self.check_index(pq)

    def test_insert_pop(self):
        # sequences of operations
        pq = pqd()
        self.check_heap_invariant(pq)
        self.check_index(pq)

        items = generateData('int')

        # push in a sequence of items
        added_items = []
        for dkey, pkey in items:
            pq.additem(dkey, pkey)
            self.check_heap_invariant(pq)
            self.check_index(pq)
            added_items.append( (dkey,pkey) )

        # pop out all the items
        popped_items = []
        while pq:
            dkey_pkey = pq.popitem()
            self.check_heap_invariant(pq)
            self.check_index(pq)
            popped_items.append(dkey_pkey)

        self.assertTrue(len(pq.heap)==0)
        self.check_index(pq)

    def test_update_remove(self):
        pq = pqd()
        self.check_heap_invariant(pq)
        self.check_index(pq)

        items = generateData('int')
        dkeys, pkeys = zip(*items)

        # heapify a sequence of items
        pq = pqd(items)

        for oper in range(100):
            if oper & 1: #update random item
                dkey = random.choice(dkeys)
                p_new = random.randrange(25)
                pq[dkey] = p_new
                self.assertTrue(pq[dkey]==p_new)
            elif pq: #delete random item
                dkey = random.choice(list(pq.keys()))
                del pq[dkey]
                self.assertTrue(dkey not in pq)
            self.check_heap_invariant(pq)
            self.check_index(pq)

    def test_heapsort(self):
        for trial in range(100):
            size = random.randrange(1,50)
            items = generateData('float', size)
            dkeys, pkeys = zip(*items)

            if trial & 1:     # Half of the time, use heapify
                pq = pqd(items)
            else:             # The rest of the time, insert items sequentially
                pq = pqd()
                for dkey, pkey in items:
                   pq[dkey] = pkey

            # NOTE: heapsort is NOT a stable sorting method, so dkeys with equal priority keys
            # are not guaranteed to have the same order as in the original sequence.
            pkeys_heapsorted = [pq.popitem()[1] for i in range(size)]
            self.assertEqual(pkeys_heapsorted, sorted(pkeys))


if __name__ == '__main__':
    unittest.main()


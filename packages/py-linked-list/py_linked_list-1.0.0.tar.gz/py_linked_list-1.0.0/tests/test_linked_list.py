# This file contains the test cases for the Linked List implementation.

# Compare this snippet from tests/test_linked_list.py:
# import unittest
# from Linked_List import LinkedList
# from Linked_List import ListNode


import unittest
from src.linked_list.Linked_List import LinkedList

class TestLinkedList(unittest.TestCase):
    def test_push(self):
        ll = LinkedList()
        ll.push(1)
        ll.push(2)
        ll.push(3)
        self.assertEqual(ll.printList(), [3, 2, 1])

    def test_append(self):
        ll = LinkedList()
        ll.append(1)
        ll.append(2)
        ll.append(3)
        self.assertEqual(ll.printList(), [1, 2, 3])

    def test_insert(self):
        ll = LinkedList()
        ll.append(1)
        ll.append(2)
        ll.append(3)
        ll.insert(2, 4)
        self.assertEqual(ll.printList(), [1, 2, 4, 3])

    def test_remove(self):
        ll = LinkedList()
        ll.append(1)
        ll.append(2)
        ll.append(3)
        ll.remove(2)
        self.assertEqual(ll.printList(), [1, 3])

    def test_remove_head(self):
        ll = LinkedList()
        ll.append(1)
        ll.append(2)
        ll.append(3)
        ll.remove(1)
        self.assertEqual(ll.printList(), [2, 3])
    
    def test_remove_tail(self):
        ll = LinkedList()
        ll.append(1)
        ll.append(2)
        ll.append(3)
        ll.remove(3)
        self.assertEqual(ll.printList(), [1, 2])
    
    def test_remove_all(self):
        ll = LinkedList()
        ll.append(1)
        ll.append(1)
        ll.append(1)
        ll.remove(1)
        self.assertEqual(ll.printList(), [])
    
    def test_remove_empty(self):
        ll = LinkedList()
        ll.remove(1)
        self.assertEqual(ll.printList(), [])
    
    def test_insert_empty(self):
        ll = LinkedList()
        ll.insert(1, 1)
        self.assertEqual(ll.printList(), [])
    
    def test_insert_not_found(self):
        ll = LinkedList()
        ll.append(1)
        ll.insert(2, 1)
        self.assertEqual(ll.printList(), [1])
    
    def test_insert_head(self):
        ll = LinkedList()
        ll.append(1)
        ll.append(2)
        ll.insert(1, 3)
        self.assertEqual(ll.printList(), [1, 3, 2])
    
    def test_insert_tail(self):
        ll = LinkedList()
        ll.append(1)
        ll.append(2)
        ll.insert(2, 3)
        self.assertEqual(ll.printList(), [1, 2, 3])
    
    def test_insert_middle(self):
        ll = LinkedList()
        ll.append(1)
        ll.append(2)
        ll.append(3)
        ll.insert(2, 4)
        self.assertEqual(ll.printList(), [1, 2, 4, 3])
    
    def test_insert_duplicate(self):
        ll = LinkedList()
        ll.append(1)
        ll.append(2)
        ll.append(3)
        ll.insert(2, 2)
        self.assertEqual(ll.printList(), [1, 2, 2, 3])

if __name__ == '__main__':
    unittest.main()

class Node:
    def __init__(self, data=None, next=None):
        self.data = data
        self.next = next
    
class Linked_list:
    def __init__(self):
        self.head = None
        self.tail = None

    def add_to_front(self, data):
        node = Node(data)
        node.next = self.head
        self.head = node
        if self.is_empty():
            self.tail = node

    def add_to_back(self, data):
        node = Node(data)
        if not self.is_empty():
            self.tail.next = node
        self.tail = node
        if self.is_empty():
            self.head = node
     
    def remove_front(self):
        if self.is_empty():
            return
        self.head = self.head.next

    def remove_back(self):
        if self.is_empty():
            return
        if self.head == self.tail and not self.is_empty():
            self.head = self.tail = None
            return
        current = self.head
        while current.next != self.tail:
            current = current.next
        current.next = None
        self.tail = current

    def is_empty(self):
        return self.head is None
    def print(self):
        current = self.head
        while current is not None:
            print(current.data, end=' ')
            current = current.next
        print()

lista = Linked_list()
lista.add_to_back(2)
lista.add_to_back(3)
lista.add_to_front(1)
lista.remove_front()
lista.add_to_front(12)
lista.remove_back()
lista.print()
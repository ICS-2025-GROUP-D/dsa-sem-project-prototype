
# ===================== Doubly Linked List for Matches =====================

class MatchNode:
    def __init__(self, position):
        self.position = position
        self.prev = None
        self.next = None

class MatchLinkedList:
    def __init__(self):
        self.head = None
        self.current = None

    def clear(self):
        self.head = None
        self.current = None

    def add(self, position):
        new_node = MatchNode(position)
        if self.head is None:
            self.head = new_node
            self.current = new_node
        else:
            temp = self.head
            while temp.next:
                temp = temp.next
            temp.next = new_node
            new_node.prev = temp

    def go_next(self):
        if self.current and self.current.next:
            self.current = self.current.next
            return self.current.position
        return None

    def go_prev(self):
        if self.current and self.current.prev:
            self.current = self.current.prev
            return self.current.position
        return None

    def get_current(self):
        return self.current.position if self.current else None

    def match_count(self):
        current = self.head
        count = 0
        while current is not None:
            count += 1
            current = current.next
        return count
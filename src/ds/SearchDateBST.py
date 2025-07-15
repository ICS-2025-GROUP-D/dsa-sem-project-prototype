
# =============== Binary search tree for searching by date ===============

class DateEntryNode:
    def __init__(self, date_str):
        self.date = date_str.split()[0]
        self.left = None
        self.right = None

class SearchDateBST:
    def __init__(self):
        self.root = None

    def insert(self, date_str):
        date_only = date_str.split()[0]
        self.root = self._insert_recursive(self.root, date_only)

    def _insert_recursive(self, node, date_str):
        if node is None:
            return DateEntryNode(date_str)
        if date_str < node.date:
            node.left = self._insert_recursive(node.left, date_str)
        elif date_str > node.date:
            node.right = self._insert_recursive(node.right, date_str)
        return node

    def search(self, date_str):
        date_only = date_str.split()[0]
        return self._search_recursive(self.root, date_only)

    def _search_recursive(self, node, date_str):
        if node is None:
            return None
        if date_str == node.date:
            return node.date
        elif date_str < node.date:
            return self._search_recursive(node.left, date_str)
        else:
            return self._search_recursive(node.right, date_str)
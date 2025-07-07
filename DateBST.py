
# =============== Binary search tree for searching by date ===============

class DateEntryNode:
    def __init__(self, date_str, entry_id):
        self.date = date_str.split()[0]
        self.entry_id = entry_id
        self.left = None
        self.right = None

class DateBST:
    def __init__(self):
        self.root = None

    def insert(self, date_str, entry_id):
        date_only = date_str.split()[0]
        self.root = self._insert_recursive(self.root, date_only, entry_id)

    def _insert_recursive(self, node, date_str, entry_id):
        if node is None:
            return DateEntryNode(date_str, entry_id)
        if date_str < node.date:
            node.left = self._insert_recursive(node.left, date_str, entry_id)
        elif date_str > node.date:
            node.right = self._insert_recursive(node.right, date_str, entry_id)
        return node

    def search(self, date_str):
        date_only = date_str.split()[0]
        return self._search_recursive(self.root, date_only)

    def _search_recursive(self, node, date_str):
        if node is None:
            return None
        if date_str == node.date:
            return node.entry_id
        elif date_str < node.date:
            return self._search_recursive(node.left, date_str)
        else:
            return self._search_recursive(node.right, date_str)
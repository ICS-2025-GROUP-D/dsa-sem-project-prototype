
# ===================== Stack for Undo/Redo functionality =====================

class UndoRedoStack:
    def __init__(self):
        self.items = []

    def is_empty(self):
        return len(self.items) == 0

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if self.is_empty():
            raise Exception("Cannot pop an empty stack")
        return self.items.pop()

    def clear(self):
        self.items = []

# ===================== Queue for replacing text occurrences ====================

class ReplaceQueue:
    def __init__(self):
        self._data = []

    def __len__(self):
        return len(self._data)

    def is_empty(self):
        return len(self._data) == 0

    def first(self):
        if self.is_empty():
            raise Exception("Queue is empty")
        return self._data[0]

    def dequeue(self):
        if self.is_empty():
            raise Exception("Queue is empty")
        return self._data.pop(0)

    def enqueue(self, e):
        self._data.append(e)
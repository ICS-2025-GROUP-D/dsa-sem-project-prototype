
# =============== Hash Table for each entry's mood ===============

class MoodHashTable:
    def __init__(self):
        self.default_tags = []
        self.tag_index = {tag: [] for tag in self.default_tags}

    def add_entry(self, tag, entry):
        if tag not in self.tag_index:
            self.tag_index[tag] = []
        self.tag_index[tag].append(entry)

    def get_entries(self, tag):
        return self.tag_index.get(tag, [])

    def remove_entry(self, tag, entry):
        if tag in self.tag_index and entry in self.tag_index[tag]:
            self.tag_index[tag].remove(entry)

    def clear(self):
        self.tag_index = {tag: [] for tag in self.default_tags}

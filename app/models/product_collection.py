class ProductCollection:
    def __init__(self, items: list):
        self.items = items

    def __iter__(self):
        return iter(self.items)

    def __len__(self):
        return len(self.items)

    def __getitem__(self, index):
        return self.items[index]

    def add(self, item):
        self.items.append(item)

    def to_json(self):
        return [item.to_json() for item in self.items]

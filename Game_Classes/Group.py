class Group(list):
    def add(self, elem):
        self.append(elem)

    def update(self, *args, **kwargs):
        for elem in self:
            elem.update(*args, **kwargs)

    def reset(self, *args, **kwargs):
        for elem in self:
            elem.reset(*args, **kwargs)
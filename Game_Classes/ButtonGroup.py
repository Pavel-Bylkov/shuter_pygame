class ButtonGroup(list):
    def add(self, button) -> None:
        super().append(button)

    def reset(self, *args, **kwargs):
        for button in self:
            button.reset(*args, **kwargs)

    def update(self, *args, **kwargs):
        for button in self:
            button.update(*args, **kwargs)

    def show(self, *args, **kwargs):
        for button in self:
            button.show(*args, **kwargs)

    def hide(self, *args, **kwargs):
        for button in self:
            button.hide(*args, **kwargs)
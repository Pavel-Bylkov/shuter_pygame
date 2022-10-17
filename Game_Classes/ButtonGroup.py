from Game_Classes.Button import Button

class ButtonGroup(list):
    def add(self, button) -> None:
        super().append(button)

    def reset(self, *args, **kwargs):
        for button in self:
            button.reset(*args, **kwargs)

    def update(self, *args, **kwargs):
        current_active = False
        last_activ = []
        for button in self:
            if isinstance(button, Button):
                active = button.active
                if active:
                    last_activ.append(button)
                button.update(*args, **kwargs)
                if active != button.active:
                    current_active = True
            else:
                button.update(*args, **kwargs)
        if len(last_activ) and current_active:
            for button in last_activ:
                button.not_active()

    def show(self, *args, **kwargs):
        for button in self:
            button.show(*args, **kwargs)

    def hide(self, *args, **kwargs):
        for button in self:
            button.hide(*args, **kwargs)
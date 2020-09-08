from kivymd.uix.dialog import MDDialog


class EndGameDialog(MDDialog):
    closing = False
    auto_dismiss = False

    def on_dismiss(self):
        return self.closing

    def close(self):
        self.closing = True
        self.dismiss(force=True)
        self.closing = False

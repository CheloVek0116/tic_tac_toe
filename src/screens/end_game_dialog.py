from kivymd.uix.dialog import MDDialog


class EndGameDialog(MDDialog):
    closing = False
    auto_dismiss = False

    def on_dismiss(self):
        # выполняется при закрытии диалога
        # если вернет True, то диалог закроется
        # Если вернет False, то не закроется
        return self.closing

    def close(self):
        self.closing = True
        self.dismiss(force=True)
        self.closing = False

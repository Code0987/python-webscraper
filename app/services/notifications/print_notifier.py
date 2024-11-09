from .notifier import Notifier


class PrintNotifier(Notifier):
    def notify(self, message: str):
        print(f"[Notification] {message}")

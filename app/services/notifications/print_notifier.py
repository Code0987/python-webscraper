from .notifier import Notifier


class PrintNotifier(Notifier):
    def notify(self, message: str) -> None:
        print(f"[Notification] {message}")

class Observer:

    def update(self, arg):
        pass


class Subject:

    def __init__(self):
        self.observers = []

    def notify(self):
        for observer in self.observers:
            observer.update(self)
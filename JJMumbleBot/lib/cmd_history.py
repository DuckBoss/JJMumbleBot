from collections import deque

class CMDQueue:

    queue_storage = None
    queue_size = 0

    def __init__(self, max_size):
        # print("Queue Initialized...")
        self.queue_storage = deque([], maxlen=max_size)

    def insert(self, item):
        if self.queue_size < self.queue_storage.maxlen:
            self.queue_storage.appendleft(item)
            self.queue_size += 1
        else:
            self.queue_storage.pop()
            self.queue_storage.appendleft(item)
            # print("added item to queue")

    def size(self):
        return self.queue_size

    def clear(self):
        self.queue_storage.clear()
        self.queue_size = 0

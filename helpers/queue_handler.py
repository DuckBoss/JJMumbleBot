import collections
from random import shuffle

class QueueHandler:

    queue_storage = None
    queue_size = 0

    def __init__(self, max_size):
        # print("Queue Initialized...")
        self.queue_storage = collections.deque([], maxlen=max_size)

    def insert_priority(self, item):
        if not self.is_full():
            self.queue_storage.append(item)
            self.queue_size += 1
            # print("added priority item to queue")

    def insert(self, item):
        if not self.is_full():
            self.queue_storage.appendleft(item)
            self.queue_size += 1
            # print("added item to queue")

    def pop(self):
        if not self.is_empty():
            item = self.queue_storage.pop()
            self.queue_size -= 1
            # print("popped item from queue")
            return item

    def is_full(self):
        if self.queue_size < self.queue_storage.maxlen:
            return False
        return True

    def is_empty(self):
        if self.queue_size <= 0:
            return True
        return False

    def shuffle(self):
        if not self.is_empty():
            shuffle(self.queue_storage)
            return True
        return False

    def remove(self, index):
        if not self.is_empty():
            temp_list = []
            while not self.is_empty():
                temp_list.append(self.pop())
            ret_val = temp_list.pop(index)
            for i, item in enumerate(temp_list):
                self.insert(item)
            return ret_val
        return None

    def size(self):
        return self.queue_size

    def clear(self):
        self.queue_storage.clear()
        self.queue_size = 0

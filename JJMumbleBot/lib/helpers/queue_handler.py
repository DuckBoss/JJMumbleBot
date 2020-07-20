import collections
from random import shuffle


class QueueHandler(collections.deque):
    queue_size = 0

    def __init__(self, iterable, maxlen):
        super(QueueHandler, self).__init__(iterable, maxlen)

    def __str__(self):
        return str(list(self))

    def to_list(self):
        return list(self)

    def insert_priority_item(self, item):
        if not self.is_full():
            self.append(item)
            self.queue_size += 1

    def insert_item(self, item):
        if not self.is_full():
            self.appendleft(item)
            self.queue_size += 1

    def pop_item(self):
        if not self.is_empty():
            item = self.pop()
            self.queue_size -= 1
            return item

    def is_full(self):
        if self.queue_size < self.maxlen:
            return False
        return True

    def is_empty(self):
        if self.queue_size <= 0:
            return True
        return False

    def shuffle(self):
        if not self.is_empty():
            shuffle(self)
            return True
        return False

    def remove_item(self, index):
        if not self.is_empty():
            temp_list = []
            while not self.is_empty():
                temp_list.append(self.pop())
            ret_val = temp_list.pop(index)
            for i, item in enumerate(temp_list):
                self.insert_item(item)
            return ret_val
        return None

    def size(self):
        return self.queue_size

    def clear(self):
        self.clear()
        self.queue_size = 0

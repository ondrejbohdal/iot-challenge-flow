import array

# A ringbuffer for data streams
class Ring:
    def __init__(self, tp, size):
        self._data = array.array(tp, [0]*size)
        self._size = size
        self._i = 0

    # Pushes a value onto the ringbuffer
    def push(self, val):
        self._data[self._i] = val
        self._i = (self._i+1) % self._size

    # Returns the n-th most recently pushed value
    def prev(self, n=0):
        return self._data[(self._i-n-1) % self._size]

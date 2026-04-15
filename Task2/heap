class MaxHeap:#max heap (priority queue), it always keeps the largest item at the top.
    def __init__(self):
        self.heap = []

    def parent(self, i):
        return (i - 1) // 2

    def left(self, i):
        return 2 * i + 1

    def right(self, i):
        return 2 * i + 2

    def insert(self, item): #add a new item into the heap
        self.heap.append(item)
        self._heapify_up(len(self.heap) - 1)

    def extract_max(self): #remove and return the largest item
        if len(self.heap) == 0:
            return None
        if len(self.heap) == 1:
            return self.heap.pop()

        root = self.heap[0]
        self.heap[0] = self.heap.pop()
        self._heapify_down(0)
        return root

    def _heapify_up(self, i):
        parent = self.parent(i)
        if i > 0 and self.heap[i][1] > self.heap[parent][1]:
            self.heap[i], self.heap[parent] = self.heap[parent], self.heap[i]
            self._heapify_up(parent)

    def _heapify_down(self, i):
        largest = i
        left = self.left(i)
        right = self.right(i)

        if left < len(self.heap) and self.heap[left][1] > self.heap[largest][1]:
            largest = left
        if right < len(self.heap) and self.heap[right][1] > self.heap[largest][1]:
            largest = right

        if largest != i:
            self.heap[i], self.heap[largest] = self.heap[largest], self.heap[i]
            self._heapify_down(largest)

    def get_size(self):
        return len(self.heap)

def heap_sort(arr): #heap sort (O(n log n))
    heap = MaxHeap()
    for item in arr:
        heap.insert(item)
    
    sorted_arr = []
    while heap.get_size() > 0:
        sorted_arr.append(heap.extract_max())
    return sorted_arr

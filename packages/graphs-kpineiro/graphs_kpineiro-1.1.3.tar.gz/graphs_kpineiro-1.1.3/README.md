Overview

* Heap: A special kind of binary tree where the parent node is always smaller than its child nodes.
* The smallest element is always at the top (heap[0]).
* Heaps are useful for efficiently managing priority queues.

Key Functions
* heappush(heap, item): Adds an item to the heap while maintaining its order.
* heappop(heap): Removes and returns the smallest item from the heap.
* heapify(x): Converts a list into a heap in place.
* heappushpop(heap, item): Adds an item to the heap, then removes and returns the smallest item.
* heapreplace(heap, item): Removes and returns the smallest item, then adds the new item to the heap.
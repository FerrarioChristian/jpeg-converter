from collections import Counter
import heapq
import numpy as np

class Node:
    def __init__(self, prob, symbol, left=None, right=None):
        self.prob = prob
        self.symbol = symbol
        self.left = left
        self.right = right
        
    def __lt__(self, other):
        return self.prob < other.prob

def calculate_huffman_size(image_matrix):
    """
    Simulates Huffman coding on the quantized DCT coefficients
    to estimate the true compressed file size in bytes.
    """
    # In JPEG, coefficients are quantized to integers.
    # We round them to simulate this step for the entropy calculation.
    data = np.round(image_matrix).astype(int).flatten()
    
    freq = Counter(data)
    heap = [Node(freq[sym], sym) for sym in freq]
    heapq.heapify(heap)
    
    if len(heap) == 0:
        return 0
    if len(heap) == 1:
        # if only one symbol (e.g. all zeros), 1 bit per symbol is a safe baseline
        return len(data) / 8.0
        
    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        parent = Node(left.prob + right.prob, None, left, right)
        heapq.heappush(heap, parent)
        
    total_bits = 0
    def traverse(node, depth):
        nonlocal total_bits
        if node.symbol is not None:
            total_bits += depth * freq[node.symbol]
        else:
            traverse(node.left, depth + 1)
            traverse(node.right, depth + 1)
            
    traverse(heap[0], 0)
    
    return total_bits / 8.0

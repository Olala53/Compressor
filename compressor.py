import heapq
from collections import defaultdict
from math import log2

class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

def build_huffman_tree(freq_dict):
    priority_queue = [HuffmanNode(char, freq) for char, freq in freq_dict.items()]
    heapq.heapify(priority_queue)

    while len(priority_queue) > 1:
        left = heapq.heappop(priority_queue)
        right = heapq.heappop(priority_queue)

        internal_node = HuffmanNode(None, left.freq + right.freq)
        internal_node.left = left
        internal_node.right = right

        heapq.heappush(priority_queue, internal_node)

    return priority_queue[0]

def build_huffman_codes(root, current_code, codes):
    if root:
        if root.char is not None:
            codes[root.char] = current_code
        build_huffman_codes(root.left, current_code + '0', codes)
        build_huffman_codes(root.right, current_code + '1', codes)

def huffman_compress(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as file:
        text = file.read()

    freq_dict = defaultdict(int)
    for char in text:
        freq_dict[char] += 1

    root = build_huffman_tree(freq_dict)
    codes = {}
    build_huffman_codes(root, '', codes)

    compressed_text = ''.join(codes[char] for char in text)

    with open(output_file, 'w') as file:
        file.write(compressed_text)

if __name__ == "__main__":
    input_file = "romeo_and_juliet.txt"
    huffman_output_file = "romeo_and_juliet.huf"

    # Huffman Compression
    with open(input_file, 'r', encoding='utf-8') as file:
        text = file.read()

    freq_dict = defaultdict(int)
    for char in text:
        freq_dict[char] += 1

    root = build_huffman_tree(freq_dict)
    huffman_codes = {}
    build_huffman_codes(root, '', huffman_codes)

    huffman_compressed_text = ''.join(huffman_codes[char] for char in text)

    with open(huffman_output_file, 'w') as file:
        file.write(huffman_compressed_text)

    # Analysis and Report
    original_bits = len(text) * 8  # Number of bits in the original text file

    huffman_bits = len(huffman_compressed_text)

    huffman_avg_length = huffman_bits / len(text)

    entropy = sum((-freq / len(text)) * (log2(freq / len(text))) for freq in freq_dict.values())

    efficiency_huffman = original_bits / huffman_bits * 100

    print("Huffman Average Code Length:", huffman_avg_length)
    print("Entropy:", entropy)
    print("Efficiency of Huffman Compression:", efficiency_huffman, "%")

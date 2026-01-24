"""
Construction naive d'un Suffix Tree en deux phases
Phase 1 : construction du TRIE des suffixes
Phase 2 : compression des chemins
Complexité : O(n^2)
"""

class TrieNode:
    def __init__(self):
        self.children = {}
        self.suffix_index = -1

def build_suffix_trie(text):
    """
    Construit le trie des suffixes du texte.
    Complexité : O(n^2)
    """
    if not text.endswith('$'):
        text += '$'
    
    root = TrieNode()
    n = len(text)
    
    for i in range(n):
        node = root
        for j in range(i, n):
            c = text[j]
            if c not in node.children:
                node.children[c] = TrieNode()
            node = node.children[c]
        node.suffix_index = i
    
    return root, text

class SuffixNode:
    def __init__(self, start, end):
        self.children = {}
        self.start = start
        self.end = end
        self.suffix_index = -1
        self.cv = -1

def compress_trie_to_tree(trie_node, text, depth=0):
    """
    Compresse récursivement un trie en suffix tree.
    """
    if depth == 0:
        root = SuffixNode(-1, -1)
        for char, child in trie_node.children.items():
            compressed_child = compress_trie_to_tree(child, text, 0)
            if compressed_child:
                root.children[char] = compressed_child
        return root

    current = trie_node
    length = 0

    while len(current.children) == 1 and current.suffix_index == -1:
        child = list(current.children.values())[0]
        current = child
        length += 1

    suffix_index = current.suffix_index
    if suffix_index == -1:
        tmp = current
        while tmp.suffix_index == -1:
            tmp = list(tmp.children.values())[0]
        suffix_index = tmp.suffix_index

    start = suffix_index + depth
    end = start + length

    new_node = SuffixNode(start, end)
    new_node.suffix_index = current.suffix_index

    for char, child in current.children.items():
        compressed_child = compress_trie_to_tree(child, text, depth + length + 1)
        if compressed_child:
            new_node.children[char] = compressed_child

    return new_node


class SuffixTree:
    def __init__(self, text):
        self.trie_root, self.text = build_suffix_trie(text)
        
        self.root = compress_trie_to_tree(self.trie_root, self.text)
        self.size = len(self.text)

def compute_cv(node):
    """
    C_v = plus petit suffix_index dans le sous-arbre.
    """
    if not node.children:
        node.cv = node.suffix_index
        return node.cv
    
    min_cv = float('inf')
    
    for child in node.children.values():
        child_cv = compute_cv(child)
        min_cv = min(min_cv, child_cv)
    
    node.cv = min_cv
    return node.cv
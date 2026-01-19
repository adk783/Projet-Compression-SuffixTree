text = ""
root = None

class Node:
    def __init__(self, start=-1, end=None):
        self.children = {}
        self.start = start
        self.end = [end] if end is not None else [-1] 
        self.suffix_index = -1
        self.cv = -1

def build_suffix_tree(input_text):
    global text, root
    text = input_text

    if not text.endswith('$'):
        text += '$'
    
    n = len(text)
    root = Node()
    
    for i in range(n):
        insert_suffix(root, i)

def insert_suffix(root, suffix_start):
    global text
    node = root
    i = suffix_start
    n = len(text)
    
    while i < n:
        char_code = ord(text[i])
        
        if char_code not in node.children:
            node.children[char_code] = Node(i, n - 1)
            node.children[char_code].suffix_index = suffix_start
            return
        
        child = node.children[char_code]
        edge_start = child.start
        edge_end = child.end[0]
        edge_len = edge_end - edge_start + 1
        
        match_len = 0
        while match_len < edge_len and i + match_len < n:
            if text[edge_start + match_len] != text[i + match_len]:
                break
            match_len += 1
            
        if match_len == edge_len:
            node = child
            i += match_len
        else:
            split_end = edge_start + match_len - 1
            split_node = Node(edge_start, split_end)
            
            node.children[char_code] = split_node
            
            child.start += match_len
            split_node.children[ord(text[child.start])] = child
            
            leaf_start = i + match_len
            new_leaf = Node(leaf_start, n - 1)
            new_leaf.suffix_index = suffix_start
            
            split_node.children[ord(text[leaf_start])] = new_leaf
            return
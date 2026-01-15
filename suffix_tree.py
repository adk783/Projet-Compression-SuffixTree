"""
SUFFIX TREE MODULE : Ukkonen Algorithm 
"""

class SuffixTreeNode:
    def __init__(self, start, end):
        self.children = [None] * 256
        self.suffix_link = None
        self.start = start
        self.end = end
        self.suffix_index = -1
        self.cv = -1 

# --- Variables Globales  ---
text = []
root = None
active_node = None
active_edge = -1
active_length = 0
remaining_suffix_count = 0
leaf_end = [-1]
root_end = None
size = -1
count = 0

def new_node(start, end):
    global count
    count += 1
    node = SuffixTreeNode(start, end)
    node.suffix_link = root
    node.start = start
    node.end = end
    node.suffix_index = -1
    return node

def edge_length(n):
    return n.end[0] - n.start + 1

def walk_down(curr_node):
    global active_length, active_edge, remaining_suffix_count, text
    
    if active_length >= edge_length(curr_node):
        active_edge = ord(text[size - remaining_suffix_count + 1])
        active_length -= edge_length(curr_node)
        return True 
    return False

def extend_suffix_tree(pos):
    global leaf_end, remaining_suffix_count, last_new_node, active_node
    global active_length, active_edge, text, root
    
    leaf_end[0] = pos
    remaining_suffix_count += 1
    last_new_node = None

    while remaining_suffix_count > 0:
        if active_length == 0:
            active_edge = ord(text[pos])

        if active_node.children[active_edge] is None:
            active_node.children[active_edge] = new_node(pos, leaf_end)

            if last_new_node:
                last_new_node.suffix_link = active_node
                last_new_node = None
        else:
            next_node = active_node.children[active_edge]
            if walk_down(next_node):
                active_node = next_node 
                continue

            if text[next_node.start + active_length] == text[pos]:
                if last_new_node and active_node != root:
                    last_new_node.suffix_link = active_node
                    last_new_node = None
                active_length += 1
                break

            split_end = [next_node.start + active_length - 1]
            split_node = new_node(next_node.start, split_end)
            
            active_node.children[active_edge] = split_node
            
            split_node.children[ord(text[pos])] = new_node(pos, leaf_end)
            
            next_node.start += active_length
            
            split_node.children[ord(text[next_node.start])] = next_node

            if last_new_node:
                last_new_node.suffix_link = split_node

            last_new_node = split_node

        remaining_suffix_count -= 1
        if active_node == root and active_length > 0:
            active_length -= 1
            active_edge = ord(text[pos - remaining_suffix_count + 1])
        elif active_node != root:
            active_node = active_node.suffix_link

def set_suffix_index_by_dfs(n, label_height):
    global size
    if not n:
        return

    # Est-ce une feuille ?
    is_leaf = True
    for i in range(256):
        if n.children[i]:
            is_leaf = False
            set_suffix_index_by_dfs(n.children[i], label_height + edge_length(n.children[i]))

    if is_leaf:
        n.suffix_index = size - label_height

def build_suffix_tree(input_text):
    """Fonction principale à appeler pour construire l'arbre"""
    global size, root_end, root, active_node, remaining_suffix_count, active_length, active_edge, leaf_end, text, count

    text = list(input_text)
    size = len(text)
    root_end = [-1]
    root = new_node(-1, root_end)
    active_node = root
    remaining_suffix_count = 0
    active_length = 0
    active_edge = -1
    leaf_end = [-1]

    for i in range(size):
        extend_suffix_tree(i)
        
    label_height = 0
    set_suffix_index_by_dfs(root, label_height)
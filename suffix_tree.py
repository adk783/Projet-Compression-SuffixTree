"""
Algorithme d'Ukkonen
Implémentation optimisée O(n) pour la compression de texte.
"""

class SuffixNode:
    def __init__(self, start: int, end: list | int):
        self.start = start
        self.end = end  
        self.children = {}
        self.suffix_link = None
        self.suffix_index = -1

class SuffixTree:
    def __init__(self, text: str):
        if not text.endswith('$'):
            text += '$'

        self.text = text
        self.size = len(text)
        
        self.root = None 
        self.root = self._new_node(-1, [-1])
        self.root.suffix_link = self.root
        
        self.active_node = self.root
        self.active_edge = -1
        self.active_length = 0
        
        self.remaining_suffix_count = 0
        
        self.leaf_end = [-1]
        
        self.last_new_node = None
        
        # Construction de l'arbre
        self._build()

    def _new_node(self, start, end):
        node = SuffixNode(start, end)
        if self.root is not None:
            node.suffix_link = self.root
        else:
            node.suffix_link = None
        return node

    def _edge_length(self, node):
        if isinstance(node.end, list):
            end_val = node.end[0]
        else:
            end_val = node.end
        return end_val - node.start + 1

    def _walk_down(self, current_node):
        """
        si active_length dépasse la longueur de l'arête, on descend vers le noeud enfant
        """
        edge_len = self._edge_length(current_node)
        if self.active_length >= edge_len:
            self.active_edge += edge_len
            self.active_length -= edge_len
            self.active_node = current_node
            return True
        return False

    def _extend(self, pos):
        """
        Phase d'extension : on ajoute le caractère à la position pos
        """
        self.leaf_end[0] = pos 
        self.remaining_suffix_count += 1
        self.last_new_node = None

        while self.remaining_suffix_count > 0:
            if self.active_length == 0:
                self.active_edge = pos

            edge_char = self.text[self.active_edge]
            
            if edge_char not in self.active_node.children:
                self.active_node.children[edge_char] = self._new_node(pos, self.leaf_end)
                
                if self.last_new_node:
                    self.last_new_node.suffix_link = self.active_node
                    self.last_new_node = None

            else:
                next_node = self.active_node.children[edge_char]
                
                if self._walk_down(next_node):
                    continue

                if self.text[next_node.start + self.active_length] == self.text[pos]:
                    if self.last_new_node and self.active_node != self.root:
                        self.last_new_node.suffix_link = self.active_node
                        self.last_new_node = None
                    
                    self.active_length += 1
                    break 

                split_end = [next_node.start + self.active_length - 1]
                split_node = self._new_node(next_node.start, split_end)
                
                self.active_node.children[edge_char] = split_node
                
                split_node.children[self.text[pos]] = self._new_node(pos, self.leaf_end)
                
                next_node.start += self.active_length
                split_node.children[self.text[next_node.start]] = next_node

                if self.last_new_node:
                    self.last_new_node.suffix_link = split_node
                self.last_new_node = split_node

            self.remaining_suffix_count -= 1
            
            if self.active_node == self.root and self.active_length > 0:
                self.active_length -= 1
                self.active_edge = pos - self.remaining_suffix_count + 1
            elif self.active_node != self.root:
                self.active_node = self.active_node.suffix_link

    def _set_suffix_indices(self, node, height):
        """
        Parcours en profondeur pour calculer l'index de départ de chaque suffixe.
        Utilisé pour retrouver les positions des motifs.
        """
        if not node.children:
            node.suffix_index = self.size - height
            return

        for child in node.children.values():
            child_edge_length = self._edge_length(child)
            self._set_suffix_indices(child, height + child_edge_length)

    def _build(self):
        for i in range(self.size):
            self._extend(i)
        self._set_suffix_indices(self.root, 0)
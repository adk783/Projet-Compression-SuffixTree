"""
Algorithme Naïf de construction du Suffix Tree
Complexité : O(n^2)
"""

class SuffixNode:
    def __init__(self, start, end=None):
        self.children = {}
        self.start = start
        self.end = [end] if end is not None else [-1]
        self.suffix_index = -1
        self.cv = -1

class SuffixTree:
    def __init__(self, text):
        self.text = text if text.endswith('$') else text + '$'
        self.size = len(self.text)
        
        # Racine
        self.root = SuffixNode(-1, -1)
        
        # Construction Naïve en O(n^2)
        for i in range(self.size):
            self._insert_suffix(i)
        
        # Compression des chemins (étape cruciale !)
        self._compress_paths()
    
    def _insert_suffix(self, suffix_start):
        """Insère le suffixe commençant à suffix_start dans l'arbre."""
        node = self.root
        pos = suffix_start  # Position courante dans le texte
        
        while pos < self.size:
            char = self.text[pos]
            
            # L'arête n'existe pas, on crée une feuille
            if char not in node.children:
                new_leaf = SuffixNode(pos, self.size - 1)
                new_leaf.suffix_index = suffix_start
                node.children[char] = new_leaf
                return
            
            # L'arête existe, on doit la parcourir
            child = node.children[char]
            edge_start = child.start
            edge_end = child.end[0]
            edge_length = edge_end - edge_start + 1
            
            # On compare caractère par caractère jusqu'à trouver une différence
            j = 0
            while j < edge_length and (pos + j) < self.size:
                if self.text[edge_start + j] != self.text[pos + j]:
                    self._split_edge(node, char, child, j, pos, suffix_start)
                    return
                j += 1
            
            node = child
            pos += edge_length
    
    def _split_edge(self, parent, edge_char, child, split_at, text_pos, suffix_start):
        """
        Sépare une arête en deux au point de divergence.
        """
        # Création du noeud de split
        split_end = child.start + split_at - 1
        split_node = SuffixNode(child.start, split_end)
        
        # Le split_node remplace l'ancien enfant dans le parent
        parent.children[edge_char] = split_node
        
        # L'ancien enfant devient fils du split_node (on décale son start)
        child.start = split_end + 1
        split_node.children[self.text[child.start]] = child
        
        # On ajoute la nouvelle feuille pour le reste du suffixe
        new_pos = text_pos + split_at
        new_leaf = SuffixNode(new_pos, self.size - 1)
        new_leaf.suffix_index = suffix_start
        split_node.children[self.text[new_pos]] = new_leaf
    
    def _compress_paths(self):
        """
        Compresse les chemins, fusionne les noeuds qui n'ont qu'un seul enfant.
        """
        self._compress_node(self.root)
    
    def _compress_node(self, node):
        """Parcours récursif pour compression."""
        # On traite d'abord les enfants
        children_to_process = list(node.children.items())
        
        for char, child in children_to_process:
            # Si le noeud a un seul enfant et n'est pas une feuille
            while len(child.children) == 1 and child.suffix_index == -1:
                # On récupère l'unique enfant
                only_char = list(child.children.keys())[0]
                only_child = child.children[only_char]
                
                # On fusionne, l'arête va maintenant de node directement à only_child
                node.children[char] = only_child
                child = only_child
            
            # Appel récursif sur le nouvel enfant
            if child.suffix_index == -1:
                self._compress_node(child)
    
    def _edge_length(self, node):
        """Calcule la longueur d'une arête."""
        if isinstance(node.end, list):
            end_val = node.end[0]
        else:
            end_val = node.end
        return end_val - node.start + 1
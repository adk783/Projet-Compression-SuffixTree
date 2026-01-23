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
        self.text = text
        self.size = len(text)

        if not text.endswith('$'):
            text += '$'
        
        # Initialisation de la racine
        self.root = self._new_node(-1, [-1])
        
        # Variables pour le point actif (active point)
        self.active_node = self.root
        self.active_edge = -1
        self.active_length = 0
        
        self.remaining_suffix_count = 0
        
        # On utilise une liste pour leaf_end au lieu d'un int car Python passe les listes par référence
        # Donc quand on modifie leaf_end[0], tous les noeuds feuilles qui pointent vers cette liste sont mis à jour automatiquement
        self.leaf_end = [-1]
        
        self.last_new_node = None
        
        # Construction de l'arbre
        self._build()

    def _new_node(self, start, end):
        node = SuffixNode(start, end)
        node.suffix_link = self.root  # Par défaut on pointe vers la racine
        return node

    def _edge_length(self, node):
        # On doit gérer le cas où end est une liste (feuille) ou un int (noeud interne)
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
        # Tous les noeuds feuilles s'étendent automatiquement
        self.leaf_end[0] = pos 
        self.remaining_suffix_count += 1
        self.last_new_node = None

        # On traite tous les suffixes restants
        while self.remaining_suffix_count > 0:
            if self.active_length == 0:
                self.active_edge = pos

            edge_char = self.text[self.active_edge]
            
            # L'arête n'existe pas encore
            if edge_char not in self.active_node.children:
                # On crée une nouvelle feuille
                self.active_node.children[edge_char] = self._new_node(pos, self.leaf_end)
                
                # Mise à jour des suffix links si nécessaire
                if self.last_new_node:
                    self.last_new_node.suffix_link = self.active_node
                    self.last_new_node = None

            else:
                # L'arête existe déjà
                next_node = self.active_node.children[edge_char]
                
                # On descend si nécessaire
                if self._walk_down(next_node):
                    continue

                # Le caractère est déjà présent dans l'arbre
                # On s'arrête
                if self.text[next_node.start + self.active_length] == self.text[pos]:
                    # On met à jour le suffix link avant de s'arrêter
                    if self.last_new_node and self.active_node != self.root:
                        self.last_new_node.suffix_link = self.active_node
                        self.last_new_node = None
                    
                    self.active_length += 1
                    break  # On arrête l'extension

                # On doit splitter l'arête existante
                # L'arête va de next_node.start à next_node.end
                # On la coupe à next_node.start + active_length - 1
                split_end = [next_node.start + self.active_length - 1]
                split_node = self._new_node(next_node.start, split_end)
                
                # Le split_node remplace next_node dans le parent
                self.active_node.children[edge_char] = split_node
                
                # On ajoute la nouvelle feuille au split_node
                split_node.children[self.text[pos]] = self._new_node(pos, self.leaf_end)
                
                # L'ancien next_node devient enfant du split_node
                # Il faut décaler son start
                next_node.start += self.active_length
                split_node.children[self.text[next_node.start]] = next_node

                # Gestion des suffix links
                if self.last_new_node:
                    self.last_new_node.suffix_link = split_node
                self.last_new_node = split_node

            self.remaining_suffix_count -= 1
            
            # Mise à jour du point actif pour le prochain suffixe
            if self.active_node == self.root and self.active_length > 0:
                # Si on est à la racine, on décale active_edge
                self.active_length -= 1
                self.active_edge = pos - self.remaining_suffix_count + 1
            elif self.active_node != self.root:
                # Sinon on suit le suffix link
                self.active_node = self.active_node.suffix_link

    def _set_suffix_indices(self, node, height):
        """
        Parcours en profondeur pour calculer l'index de départ de chaque suffixe.
        Utilisé pour retrouver les positions des motifs.
        """
        if not node.children:
            # C'est une feuille
            node.suffix_index = self.size - height
            return

        for child in node.children.values():
            child_edge_length = self._edge_length(child)
            self._set_suffix_indices(child, height + child_edge_length)

    def _build(self):
        for i in range(self.size):
            self._extend(i)
        self._set_suffix_indices(self.root, 0)
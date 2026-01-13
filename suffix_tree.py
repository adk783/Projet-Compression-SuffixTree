"""
SUFFIX TREE MODULE
------------------
This file contains the implementation of the Suffix Tree structure.
It allows building a tree from a text using a naive construction algorithm (O(n^2)).
Used as the base structure for the Ziv-Lempel compression.

Authors: [Dev1]
"""

class Node : 
    def __init__(self):
        self.children = {} # Utilisation d'un dictionnaire pour les transitions : {label: Node}

def NaiveSuffixTree(T):
    """
    Implémentation de l'algorithme NaiveSuffixTree.
    Complexité temporelle : Theta(|T|^2)
    """

    S = Node() # S <- NEWTRIE()

    if not T.endswith('$'):
        T += '$'

    # for i = 0 to |T|-1 do Insert T[i...|T|] into S
    for i in range(len(T)):
        current = S
        suffix = T[i:]
        for char in suffix:
            if char not in current.children:
                current.children[char] = Node()
            current = current.children[char]
    
    # for v node of S do if v has a single child then Merge v with its child   
    def compress_tree(v):

        labels = list(v.children.keys())

        for label in labels:
            child = v.children[label]

            compress_tree(child)
            
            # Si l'enfant n'a qu'un seul fils, on fusionne
            if len(child.children) == 1:
                grandchild_label = list(child.children.keys())[0]
                grandchild_node = child.children[grandchild_label]
                
                # Fusion
                new_label = label + grandchild_label
                v.children[new_label] = grandchild_node
                
                # On supprime l'ancien lien vers l'enfant
                del v.children[label]

    compress_tree(S)
    
    return S

def afficher_arbre(node, indent=""):
    """Fonction utilitaire pour visualiser le résultat"""
    for label, child in node.children.items():
        print(f"{indent}└── {label}")
        afficher_arbre(child, indent + "    ")

# --- Test de l'algorithme ---
if __name__ == "__main__":
    texte_test = "abac"
    print(f"Algorithme NaiveSuffixTree pour : '{texte_test}'")
    
    suffix_tree = NaiveSuffixTree(texte_test)
    afficher_arbre(suffix_tree)











    

    

       
            
            
            
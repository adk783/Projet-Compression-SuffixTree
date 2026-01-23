"""
Compression Ziv-Lempel via Suffix Tree
"""
from suffix_tree import SuffixTree

def compute_cv(node):
    """
    Calcule C_v pour chaque noeud par un parcours DFS (Post-order).
    C_v = le plus petit index de suffixe présent dans le sous-arbre du noeud.
    Cela permet de savoir si une branche contient une occurrence apparue dans le passé.
    """
    # Cas de base : c'est une feuille, son Cv est son propre index
    if not node.children:
        node.cv = node.suffix_index
        return node.cv
    
    # Cas récursif : le min des enfants
    min_cv = float('inf')
    
    for child in node.children.values():
        child_cv = compute_cv(child)
        if child_cv < min_cv:
            min_cv = child_cv
            
    node.cv = min_cv
    return min_cv

def find_longest_match(tree, current_pos):
    """
    Cherche la plus longue sous-chaîne dans l'arbre qui commence à current_pos,
    mais qui est deja apparue avant (grâce à C_v).
    Retourne (longueur du match, position de début du match dans le texte)
    """
    node = tree.root
    total_matched = 0
    best_match_pos = -1
    
    # On navigue dans l'arbre tant qu'on peut
    while True:
        # On ne doit pas dépasser la fin du texte
        if current_pos + total_matched >= tree.size - 1:
            break
            
        # Caractère qu'on cherche à matcher
        next_char = tree.text[current_pos + total_matched]
        
        # Si pas d'arête pour ce caractère, on s'arrête
        if next_char not in node.children:
            break
            
        child = node.children[next_char]
         
        # Condition importante : on ne peut descendre que si cette branchecontient une occurrence qui apparait avant current_pos
        if child.cv >= current_pos:
            break
            
        # On parcourt l'arête caractère par caractère
        edge_start = child.start
        edge_end = child.end[0] if isinstance(child.end, list) else child.end
        edge_length = edge_end - edge_start + 1
        
        chars_matched = 0
        
        for i in range(edge_length):
            text_idx = current_pos + total_matched
            edge_idx = edge_start + i
            
            # On ne dépasse pas la fin
            if text_idx >= tree.size - 1:
                break
                
            # On compare les caractères
            if tree.text[text_idx] != tree.text[edge_idx]:
                break
                
            chars_matched += 1
            total_matched += 1
            
        # Si on a matché toute l'arête, on descend vers l'enfant
        if chars_matched == edge_length:
            node = child
            best_match_pos = child.cv  # On garde la position
        else:
            # Match partiel, on s'arrête
            if chars_matched > 0:
                best_match_pos = child.cv
            break
            
    return total_matched, best_match_pos

def compress(text_input):
    """
    Exécute la compression LZ77 en utilisant le Suffix Tree.
    Retourne une liste mixte de caractères et de tuples (position, longueur).
    """
    
    # Construction de l'arbre des suffixes
    tree = SuffixTree(text_input)
    
    # Annotation des C_v pour tous les noeuds
    compute_cv(tree.root)
    
    compressed = []
    pos = 0
    text_length = tree.size - 1 
    
    while pos < text_length:
        match_length, match_start = find_longest_match(tree, pos)
        
        if match_length > 0:
            # On a trouvé une répétition passée
            compressed.append((match_start, match_length))
            pos += match_length
        else:
            # Pas de répétition trouvée, on écrit le caractère brut
            compressed.append(tree.text[pos])
            pos += 1
            
    return compressed
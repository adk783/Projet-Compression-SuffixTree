"""
Compression Ziv-Lempel via Suffix Tree
"""

from suffix_tree import SuffixTree

def compute_cv(node):

    """
    Calcule C_v.
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
    Cherche la plus longue sous-chaîne dans l'arbre qui commence à current_pos, mais qui est deja apparue avant grâce à C_v.
    Retourne (longueur du match, position de début du match dans le texte)
    """

    node = tree.root
    total_matched = 0
    best_match_pos = -1

    while True:
        if current_pos + total_matched >= tree.size - 1:
            break

        next_char = tree.text[current_pos + total_matched]

        if next_char not in node.children:
            break

        child = node.children[next_char]

        if child.cv >= current_pos:
            break

        edge_start = child.start
        edge_end = child.end[0] if isinstance(child.end, list) else child.end
        edge_length = edge_end - edge_start + 1

        chars_matched = 0

        for i in range(edge_length):
            text_idx = current_pos + total_matched
            edge_idx = edge_start + i

            if text_idx >= tree.size - 1:
                break

            if tree.text[text_idx] != tree.text[edge_idx]:
                break

            chars_matched += 1
            total_matched += 1

        if chars_matched == edge_length:
            node = child
            best_match_pos = child.cv
        else:
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
            compressed.append((match_start, match_length))
            pos += match_length
        else:
            compressed.append(tree.text[pos])
            pos += 1

    return compressed
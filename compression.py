"""
Compression Ziv-Lempel via Suffix Tree

Principe :
On parcourt le texte de gauche à droite. À chaque position, on cherche la plus
longue sous-chaîne déjà apparue auparavant. Cette recherche est accélérée
grâce au suffix tree, et la condition d'antériorité est vérifiée avec la valeur C_v.

Chaque facteur est codé soit :
- par un caractère littéral
- par un couple (position, longueur) représentant une copie LZ77.
"""

from suffix_tree import SuffixTree

def compute_cv(node):

    """
    Calcule C_v.
    
    C_v = plus petit index de suffixe dans le sous-arbre du noeud.
    Cela permet de savoir si une sous-chaîne apparaît avant une position donnée
    dans le texte.
    """

    # Cas de base : c'est une feuille, son C_v est son propre index
    if not node.children:
        node.cv = node.suffix_index
        return node.cv

    # Sinon, C_v est le minimum des C_v de ses enfants
    min_cv = float('inf')

    for child in node.children.values():
        child_cv = compute_cv(child)
        if child_cv < min_cv:
            min_cv = child_cv   

    node.cv = min_cv
    return min_cv



def find_longest_match(tree, current_pos):

    """
    Recherche, à partir de current_pos, la plus longue sous-chaîne
    déjà apparue auparavant dans le texte.

    Le suffix tree permet une recherche en temps linéaire dans la longueur du motif.
    La condition child.cv < current_pos garantit que l'occurrence est dans le passé.

    Retour :
    - longueur du match
    - position de début de la copie dans le texte
    """

    node = tree.root
    total_matched = 0
    best_match_pos = -1

    while True: # Fin du texte atteinte
        if current_pos + total_matched >= tree.size - 1:
            break

        next_char = tree.text[current_pos + total_matched]

        # Pas d'arête correspondant au caractère suivant
        if next_char not in node.children:
            break

        child = node.children[next_char]

        # Le motif n'existe que dans le futur, on ne peut pas l'utiliser
        if child.cv >= current_pos:
            break

        edge_start = child.start
        edge_end = child.end[0] if isinstance(child.end, list) else child.end
        edge_length = edge_end - edge_start + 1

        chars_matched = 0

        # Comparaison caractère par caractère le long de l'arête
        for i in range(edge_length):
            text_idx = current_pos + total_matched
            edge_idx = edge_start + i

            if text_idx >= tree.size - 1:
                break

            if tree.text[text_idx] != tree.text[edge_idx]:
                break

            chars_matched += 1
            total_matched += 1

        # Si toute l'arête est parcourue, on continue plus bas
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
    Algorithme principal de compression LZ77 basé sur suffix tree.

    Étapes :
    1. Construction du suffix tree du texte
    2. Calcul des valeurs C_v
    3. Parcours séquentiel du texte :
       - à chaque position, recherche du plus long facteur déjà vu
       - si trouvé : émission d'un couple (position, longueur)
       - sinon : émission du caractère brut
    """

    # Construction du suffix tree (Ukkonen ou version naïve selon le module chargé)
    tree = SuffixTree(text_input)

     # Calcul des C_v pour tous les noeuds
    compute_cv(tree.root)

    compressed = []
    pos = 0
    text_length = tree.size - 1 # on ignore le symbole terminal $

    while pos < text_length:
        match_length, match_start = find_longest_match(tree, pos)

        if match_length > 0:
            compressed.append((match_start, match_length)) # On encode une copie LZ77
            pos += match_length
        else:
            compressed.append(tree.text[pos]) # Aucun motif : on stocke le caractère brut
            pos += 1

    return compressed
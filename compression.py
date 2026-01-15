import suffix_tree as st

# ÉTAPE 1 : Calcul des cv
def compute_cv(node):
    """
    Calcule la position de la premiere occurrence (cv) pour chaque noeud.
    cv = plus petit index de suffixe dans le sous-arbre.
    """
    if node.suffix_index != -1:
        node.cv = node.suffix_index
        return node.cv

    min_pos = float('inf')
    
    for child in node.children:
        if child is not None:
            valeur_enfant = compute_cv(child)
            # Mise à jour du minimum
            if valeur_enfant < min_pos:
                min_pos = valeur_enfant
    
    node.cv = min_pos
    return min_pos


# ÉTAPE 2 : La Fonction de Recherche du Meilleur Match
def find_longest_match(root, text, current_index):
    """
    Trouve la plus longue chaine dans l'arbre qui respecte la condition temporelle.
    Condition : l'occurrence trouvee doit etre dans le passe (cv < current_index).
    """
    current_node = root
    longueur_match = 0
    position_depart = -1
    
    while True:
        if current_index + longueur_match >= len(text):
            break
            
        char_code = ord(text[current_index + longueur_match])
        child = current_node.children[char_code]
        
        if child is None:
            break
            
        if child.cv >= current_index:
            break
        
        edge_start = child.start
        edge_end = child.end[0]
        edge_length = edge_end - edge_start + 1
        
        match_count = 0
        match_total = True
        
        for k in range(edge_length):
            idx_text = current_index + longueur_match + k
            idx_edge = edge_start + k
            
            if idx_text >= len(text):
                match_total = False
                break
                            
            if text[idx_text] != st.text[idx_edge]:
                match_total = False
                break
            
            match_count += 1
            
        if match_total:
            longueur_match += edge_length
            current_node = child
            position_depart = child.cv
            
        else:
            longueur_match += match_count
            position_depart = child.cv 
            break
            
    return longueur_match, position_depart


# ÉTAPE 3 : La Boucle Principale de Compression
def compress(text_input):
    """
    Fonction principale.
    """
    
    print("Construction de l'arbre...")
    st.build_suffix_tree(text_input)
    
    print("Calcul des CV (Pre-traitement)...")
    compute_cv(st.root)
    
    i = 0
    resultat = []
    n = len(text_input)
    
    while i < n:
        longueur, start_pos = find_longest_match(st.root, text_input, i)
        
        if longueur > 0:
            resultat.append( (start_pos, longueur) )
            
            i = i + longueur
            
        else:
            resultat.append( text_input[i] )
            
            i = i + 1
            
    return resultat
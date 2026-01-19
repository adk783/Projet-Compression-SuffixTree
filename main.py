# -*- coding: utf-8 -*-
import compression
import os
import time 
import suffix_tree as st
import importlib
import urllib.request
import re
import unicodedata

import suffix_tree as algo_ukkonen       # L'algo rapide (O(N))
import naif_suffix_tree as algo_naif    # L'algo lent (O(N^2))

def creer_fichiers_test():
    """Cree des fichiers de tailles variees pour le test."""
    print("Creation des fichiers de test sur le disque")
    
    with open("test_banana.txt", "w", encoding="utf-8") as f:
        f.write("banananana")

    with open("test_phrase.txt", "w", encoding="utf-8") as f:
        f.write("le chat mange le chat et le chien mange le chien " * 5)

    with open("test_adn.txt", "w", encoding="utf-8") as f:
        motif_base = "AGCTTTTCATTCTGACTGCAACGGGCAATATGTCTCTGTGTGGATTAAAAAAAGAGTGTCTGATAGCAGC"
        f.write(motif_base * 150) 

    with open("test_big.txt", "w", encoding="utf-8") as f:
        paragraphe = "Ceci est un paragraphe de test qui va se repeter encore et encore pour valider la compression Ziv-Lempel via Suffix Tree. "
        f.write(paragraphe * 500)

    with open("test_ziv_lempel.txt", "w", encoding="utf-8") as f:
        texte_lz = """
        abraham lempel et jacob ziv sont les inventeurs de la compression sans perte.
        ils ont publie leur algorithme celebre dans les annees soixante dix.
        le principe est de remplacer des repetitions par des references vers le passe.
        si le mot algorithme apparait deux fois la deuxieme fois on met un lien.
        cela permet de reduire la taille du fichier sans perdre aucune information.
        le suffix tree est une structure de donnees puissante pour accelerer ce processus.
        au lieu de chercher lentement dans tout le texte le suffix tree trouve les motifs instantanement.
        cette technique est utilisee aujourdhui dans les formats zip png et gif.
        cest une revolution pour le stockage de donnees et la transmission sur internet.
        le dictionnaire se construit dynamiquement pendant la lecture du flux de donnees.
        """
        f.write(texte_lz.replace('\n', ' ').strip().lower())

    print(" Telechargement et nettoyage du livre 'Arsene Lupin'...")
    try:
        url = "https://www.gutenberg.org/cache/epub/32854/pg32854.txt"
        with urllib.request.urlopen(url) as response:
            data = response.read().decode('utf-8')
        
        data = data.lower()
        data = unicodedata.normalize('NFD', data)
        data = data.encode('ascii', 'ignore').decode('utf-8')
        data_safe = re.sub(r'[^a-z ]', '', data)
        data_safe = re.sub(r' +', ' ', data_safe)
        taille_max = 50000 
        data_final = data_safe[:taille_max]

        with open("test_livre.txt", "w", encoding="utf-8") as f:
            f.write(data_final)
        print(f"   [OK] Livre genere : {len(data_final)} caracteres.")

    except Exception as e:
        print(f"   [ERREUR] Impossible de telecharger le livre : {e}")

    print("Fichiers generes avec succes\n")

def lancer_test(nom_fichier):
    global st 
    st = importlib.reload(st)
    print(f"{'='*60}")
    print(f"TEST SUR : {nom_fichier}")
    
    if not os.path.exists(nom_fichier):
        print("Erreur : Fichier introuvable.")
        return

    with open(nom_fichier, "r", encoding="utf-8") as f:
        texte = f.read()
    
    taille_originale = len(texte)
    print(f"Taille originale : {taille_originale} caracteres")

    # Naif
    compression.st = algo_naif 
    debut_naif = time.time()
    try:
        _ = compression.compress(texte)
    except Exception as e:
        print(f"Erreur Naif : {e}")
        return
    fin_naif = time.time()
    temps_naif = fin_naif - debut_naif

    # Ukkonen
    compression.st = algo_ukkonen
    debut_ukkonen = time.time()
    try:
        resultat = compression.compress(texte)
    except Exception as e:
        print(f"Erreur Ukkonen : {e}")
        return
    fin_ukkonen = time.time()
    temps_ukkonen = fin_ukkonen - debut_ukkonen

    nb_tokens = len(resultat)
    nb_copies = 0
    nb_litteraux = 0
    
    for token in resultat:
        if isinstance(token, tuple):
            nb_copies += 1
        else:
            nb_litteraux += 1

    taux = (1 - (nb_tokens / taille_originale)) * 100

    nom_sortie = nom_fichier.replace(".txt", "_COMPRESSE.txt")
    with open(nom_sortie, "w", encoding="utf-8") as f:
        f.write(str(resultat))
    
    print(f" -> Fichier resultat cree : {nom_sortie}")

    print(f"Temps de compression NAIF    : {temps_naif:.4f} secondes")
    print(f"Temps de compression UKKONEN : {temps_ukkonen:.4f} secondes")

    if temps_ukkonen > 0:
        ratio = temps_naif / temps_ukkonen
        print(f" -> Acceleration             : x{ratio:.1f}")

    print(f"RESULTATS :")
    print(f"   - Caracteres bruts gardes : {nb_litteraux}")
    print(f"   - Remplacements (Copies)  : {nb_copies}")
    print(f"   - Taille liste compressee : {nb_tokens} items")
    print(f"   ->TAUX DE COMPRESSION : {taux:.2f} %")
    
    print(f"\n   >>> Resultat disponible dans le fichier : {nom_sortie}")

if __name__ == "__main__":
    creer_fichiers_test()
   
    lancer_test("test_banana.txt")
    lancer_test("test_phrase.txt")
    lancer_test("test_adn.txt")
    lancer_test("test_big.txt")
    lancer_test("test_ziv_lempel.txt")
    lancer_test("test_livre.txt")
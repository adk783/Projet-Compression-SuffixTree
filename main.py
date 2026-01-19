# -*- coding: utf-8 -*-
import compression
import os
import time 
import suffix_tree as st
import importlib

def creer_fichiers_test():
    """Cree des fichiers de tailles variees pour le test."""
    print("Creation des fichiers de test sur le disque...")
    
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

    debut = time.time()
    try:
        resultat = compression.compress(texte)
    except Exception as e:
        print(f"Erreur : {e}")
        return
    fin = time.time()
    
    temps_execution = fin - debut

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

    print(f"Temps de compression : {temps_execution:.4f} secondes")
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
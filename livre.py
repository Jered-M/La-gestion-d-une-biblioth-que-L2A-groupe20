from datetime import datetime, timedelta
import json

# Compter le nombre de caractères
def compterLesCaracteres(chaine):
    if len(chaine) > 5 and len(chaine) < 100 :
        return True
    else:
        return False

# Vérifier qu'on a reçu une chaine de caractère
def doitEtreUneChaine(chaine):
    if not chaine.isnumeric() :
        return True
    else:
        return False

def validerTitre(titre):
    return compterLesCaracteres(titre) and doitEtreUneChaine(titre)

def validerAuteur(auteur):
    return compterLesCaracteres(auteur) and doitEtreUneChaine(auteur)
# Valider le genre
def validerGenre(genre):
    return compterLesCaracteres(genre) and doitEtreUneChaine(genre)

# Valider les données saisies par l'utilisateur
def validerTout(titre, auteur, genre):
    if validerTitre(titre) and validerAuteur(auteur) and validerGenre(genre):
        return True
    else:
        return False

def recupererTousLesLivres() :
    try :
        with open('data/livres.json', 'r') as fichier :
            tousLesLivres = json.load(fichier) # Récupérer tous les livres

            if not isinstance(tousLesLivres, list):
                tousLesLivres = [tousLesLivres]

            fichier.close() # Fermer le fichier 
    except json.JSONDecodeError :
        tousLesLivres = []

    return tousLesLivres

def ajouterLivre():
    titre = input("Taper le titre du livre : ")
    auteur = input("Taper l'auteur : ")
    genre = input("Genre du livre : ")

    # Si tout est valider
    if validerTout(titre, auteur, genre):
        
        tousLesLivres = recupererTousLesLivres() # Récupérer tous les livres
        
        # Dérouler tous les livres
        for livre in tousLesLivres:
            # Vérifier si ce titre est déjà existant
            if livre["Titre"] == titre:
                print("Ce livre est déjà enregisté")
                return

        # L'id du prochain livre, ce le nombre de livre + 1
        if len(tousLesLivres) == 0 :
            id = 1
        else :
            dernierLivre = tousLesLivres[-1]
            id = dernierLivre["ID"] + 1

        # Créer le dictionnaire pour stocker le livre
        nouveauLivre = {
            "ID" : id,
            "Titre" : titre,
            "Auteur" : auteur,
            "Genre" : genre,
            "Disponible" : True
        }

        preparerEnregistrement(nouveauLivre)
        print("Le livre a été ajouté avec succès !")
    else:
        print("Les informations sont incorrectes !")

def preparerEnregistrement(nouveauLivre):
    # Récupérer le contenu du fichier des livres
    anciensLivres = recupererTousLesLivres()
    
    # Ajouter le nouveau livre  aux anciens
    anciensLivres.append(nouveauLivre)

    enregistrerDansLeFichier(anciensLivres)

def enregistrerDansLeFichier(nouveauxLivres):
    # Enregistrer ces informations dans le fichier
    with open("data/livres.json", "w") as fichier:
        json.dump(nouveauxLivres, fichier)
        fichier.close()

def afficherTout():
    print("Affichage des livres")
    print("0. Pour les archivés")
    print("1. Pour les disponibles")

    disponibilite = None

    while disponibilite != 0 and disponibilite != 1 :
        disponibilite = int(input("Taper votre choix : "))
    
    print("Voici tous les livres de cette catégorie")

    tousLesLivres = recupererTousLesLivres()

    livresTrouves = False

    for livre in tousLesLivres :
        if disponibilite == 0 and livre["Disponible"] == False :
            print(f"{livre}")
            livresTrouves = True
        elif disponibilite == 1 and livre["Disponible"] == True :
            print(f"{livre}")
            livresTrouves = True

    if livresTrouves == False :
        print("Aucun livre n'a été trouvé dans cette catégorie !")

def rechercherUnLivre():
    champ = None

    while champ != "Titre" and champ != "Auteur" and champ != "Genre" :
        champ = input("Taper le champ de recherche (Titre, Auteur ou Genre) : ")
        valeur = input("Taper la valeur : ")
    
    tousLesLivres = recupererTousLesLivres()

    livreTrouve = False

    for livre in tousLesLivres:
        if livre[champ] == valeur :
            livreTrouve = True
            print(livre)
    
    if livreTrouve == False :
        print("Aucun livre ne correspond à votre critère de recherche : ")

def archiverUnLivre() :
    ID = int(input("Entrer l'ID du livre :"))

    tousLesLivres = recupererTousLesLivres()
    
    livreTrouve = False
    for livre in tousLesLivres:
        if livre["ID"] == ID :
            livre["Disponible"] = False
            livreTrouve = True
    
    if livreTrouve :
        enregistrerDansLeFichier(tousLesLivres)
        print("Le livre a été archivé avec succès !")
    else :
        print("Le livre avec cet ID n'a pass été trouvé !")

def supprimerUnLivre() :
    ID = int(input("Entrer l'ID du livre :"))

    tousLesLivres = recupererTousLesLivres()
    nouveauxLivres = []

    livreTrouve = False
    for livre in tousLesLivres:
        if livre["ID"] != ID :
            nouveauxLivres.append(livre)
            livreTrouve = True
    
    if livreTrouve :
        enregistrerDansLeFichier(nouveauxLivres)
        print("Le livre a été archivé avec succès !")
    else :
        print("Le livre avec cet ID n'a pass été trouvé !")
        
def emprunter_livre():
    user_id = input("Entrez l'ID de l'utilisateur : ")
    book_title = input("Entrez le titre du livre à emprunter : ")
    borrow_date = datetime.now().strftime("%Y-%m-%d")
    return_date = (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d")  # Date de retour après 14 jours

    with open('data/users.json', "r") as f:
        users = json.load(f)

    for user in users:
        if user["id"] == int(user_id):
            if 'books_borrowed' not in user:
                user['books_borrowed'] = []

            user['books_borrowed'].append({
                'title': book_title,
                'borrow_date': borrow_date,
                'return_date': return_date
            })
                
            if 'history' not in user:
                user['history'] = []

            user['history'].append({
                'book': book_title,
                'borrow_date': borrow_date,
                'return_date': None
            })
                
            with open('data/users.json', "w") as f:
                json.dump(users, f)
                
            print(f"Le livre '{book_title}' a été emprunté par {user['name']} jusqu'au {return_date}.")
            return

    print("Utilisateur non trouvé.")
    
def retourner_livre():
    user_id = input("Entrez l'ID de l'utilisateur : ")
    book_title = input("Entrez le titre du livre à retourner : ")

    with open('data/users.json', "r") as f:
        users = json.load(f)

    for user in users:
        if user["id"] == int(user_id):
            for book in user.get('books_borrowed', []):
                if book['title'] == book_title:
                    user['books_borrowed'].remove(book)
                    for entry in user['history']:
                        if entry['book'] == book_title and entry['return_date'] is None:
                            entry['return_date'] = datetime.now().strftime("%Y-%m-%d")
                            break
                    with open('data/users.json', "w") as f:
                        json.dump(users, f)
                    print(f"Le livre '{book_title}' a été retourné par {user['name']}.")
                    return

    print("Livre ou utilisateur non trouvé.")
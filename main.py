from livre import ajouterLivre, afficherTout, rechercherUnLivre, archiverUnLivre, retourner_livre, supprimerUnLivre
from utilisateur import mange_users
from livre import emprunter_livre
from livre import retourner_livre

def menu_principal():
    choix = 0

    while 1 > choix or choix > 8 :
        print("1. Ajouter un livre")
        print("2. Rechercher un livre")
        print("3. Archiver un livre")
        print("4. Supprimer un livre")
        print("5. Afficher les livres")
        print("6. Emprunter un livre")
        print("7. Retourner un livre")
        print("8. Ajouter un utilisatreur")
        print("9. Quitter le programme")

        choix = int(input("Taper votre choix : "))
        
    return choix

def main():
    while True:
        choix = menu_principal()

        if 1 == choix:
            ajouterLivre()
        elif 2 == choix:
            rechercherUnLivre()
        elif 3 == choix:
            archiverUnLivre()
        elif 4 == choix:
            supprimerUnLivre()
        elif 5 == choix:
            afficherTout()
        elif 6 == choix:
            emprunter_livre()
        elif 7 == choix:
            retourner_livre()
        elif 8 == choix:
            mange_users()
        else:
            print("Merci d'avoir utilisé notre programme à plus !")
            break

if __name__ == "__main__":
    main()
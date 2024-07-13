import json
from datetime import datetime

def save_user(user):
    if not user.startswith(("#", "@", "$", "%", "&", "_ ")) or len(user) > 5 and len(user) < 15:
        return True
    else:
        return False


def save_user(user):
    with open("users.json", "r") as f:
        users = json.load(f)
        users.append(user)
        
    with open('users.json', 'w') as file:
        user_json = json.dumps(users)
        file.write(user_json)

def create_user():
    with open("users.json", "r") as f:
        users = json.load(f)
        if len(users) == 0:
            idUser = 1
        else:
            idUser = users[-1]["id"] + 1
        name = input("Entrer le nom du lecteur : ")
        email = input("Entrer l'email du lecteur : ")
       
        if not name or not email:
            print("Veuillez remplir tous les champs")
            return
        elif name.startswith(("#", "@", "$", "%", "&", "_ ")) :
            print("Le nom ne doit pas contenir des caractères spéciaux!")
            return
       
        user = {
            'id': idUser,
            'name': name,
            'email': email,
            'books_borrowed': []  # Ajout du champ pour les livres empruntés
        }

        save_user(user)

def show_all_users(): 
    try:
        with open("users.json", "r") as f:
            users = json.load(f)
            if len(users) == 0:
                print("Le fichier JSON est vide.")
            else:
                print("Voici la liste de tous vos lecteurs")
                print("-----------------------------------")
                for user in users:
                    print(f"\tLecteur ID: {user['id']}")
                    print(f"\tNom du lecteur: {user['name']}")
                    print(f"\tEmail: {user['email']}")

    except FileNotFoundError:
        print("Le fichier JSON n'existe pas.")
    except json.JSONDecodeError:
        print("Le fichier JSON est mal formaté.")

def delete_user():
    user_id = input("Entrez l'ID du lecteur à supprimer: ")
    with open("users.json", "r") as f:
        users = json.load(f)
    index = -1
    for i in range(len(users)):
        if users[i]["id"] == int(user_id):
            index = i
            break
    if index != -1:
        del users[index]
        with open("users.json", "w") as f:
            json.dump(users, f)
        print("Le lecteur a été supprimé.")
    else:
        print("Le lecteur non trouvé !.")

def update_user():
    user_id = input("Entrez l'ID du lecteur à modifier: ")
    with open("users.json", "r") as f:
        users = json.load(f)
    for user in users:
        if user["id"] == int(user_id):
            new_name = input(f"Entrez le nouveau nom (Actuel: {user['name']}): ")
            new_email = input(f"Entrez le nouvel email (Actuel: {user['email']}): ")
            user["name"] = new_name
            user["email"] = new_email
            with open("users.json", "w") as f:
                json.dump(users, f)
            print("Les informations de l'utilisateur ont été mises à jour.")
            return
    print("Utilisateur non trouvé.")

def show_user_books():
    user_id = input("Entrez l'ID du lecteur: ")
    with open("users.json", "r") as f:
        users = json.load(f)
    for user in users:
        if user["id"] == int(user_id):
            if 'books_borrowed' in user and len(user["books_borrowed"]) == 0:
                print(f"L'utilisateur {user['name']} n'a pas emprunté de livres.")
            elif 'books_borrowed' in user:
                print(f"Voici les livres empruntés par l'utilisateur {user['name']}:")
                for book in user["books_borrowed"]:
                    print(f"- {book}")
            else:
                print(f"L'utilisateur {user['name']} n'a pas de champ 'books_borrowed'.")
            return
    print("Utilisateur non trouvé.")

def show_user_history(user_id):
    with open("users.json", "r") as f:
        users = json.load(f)
    for user in users:
        if user["id"] == int(user_id):
            if 'history' in user and len(user["history"]) > 0:
                print(f"Voici l'historique des emprunts et retours de {user['name']} :")
                for entry in user["history"]:
                    print(f"- {entry['book']} emprunté le {entry['borrow_date']}, rendu le {entry['return_date']}")
            else:
                print(f"{user['name']} n'a pas encore d'historique d'emprunts.")
            return
    print("Utilisateur non trouvé.")

def sort_users(sort_by):
    with open("users.json", "r") as f:
        users = json.load(f)
    
    if sort_by == "name":
        users.sort(key=lambda x: x["name"])
    elif sort_by == "email":
        users.sort(key=lambda x: x["email"])
    # Ajoutez d'autres critères de tri si nécessaire
    
    print("Voici la liste des utilisateurs triés :")
    for user in users:
        print(f"ID: {user['id']}, Nom: {user['name']}, Email: {user['email']}")

def search_users():
    search_term = input("Entrez le terme de recherche (nom, email) : ")
    with open("users.json", "r") as f:
        users = json.load(f)
    
    found_users = [user for user in users if search_term.lower() in user["name"].lower() or search_term.lower() in user["email"].lower()]
    
    if found_users:
        print("Utilisateurs trouvés :")
        for user in found_users:
            print(f"ID: {user['id']}, Nom: {user['name']}, Email: {user['email']}")
    else:
        print("Aucun utilisateur trouvé.")

def show_overdue_users():
    current_date = datetime.now().strftime("%Y-%m-%d")
    with open("users.json", "r") as f:
        users = json.load(f)
    overdue_users = []
    for user in users:
        for book in user.get("books_borrowed", []):
            if book['return_date'] < current_date:
                overdue_users.append(user)
                break
    if overdue_users:
        print("Utilisateurs ayant des livres en retard :")
        for user in overdue_users:
            print(f"ID: {user['id']}, Nom: {user['name']}, Email: {user['email']}")
    else:
        print("Aucun utilisateur n'a de livres en retard.")

def choice_to_manage_users():
    print("1. Afficher tous les lecteurs")
    print("2. Ajouter un lecteur")
    print("3. Supprimer un lecteur")
    print("4. Modifier les informations d'un lecteur")
    print("5. Afficher les livres empruntés par un lecteur")
    print("6. Afficher l'historique d'un utilisateur")
    print("7. Trier les utilisateurs")
    print("8. Recherche avancée d'utilisateurs")
    print("9. Afficher les utilisateurs ayant des retards")
    choice = int(input("Sélectionnez une option : "))
    return choice

def mange_users(): 
    choice = choice_to_manage_users()
    if choice == 1: 
        show_all_users()
    elif choice == 2: 
        create_user()
    elif choice == 3:
        delete_user()
    elif choice == 4:
        update_user()
    elif choice == 5:
        show_user_books()
    elif choice == 6:
        user_id = input("Entrez l'ID de l'utilisateur : ")
        show_user_history(user_id)
    elif choice == 7:
        sort_by = input("Trier par (nom/email) : ")
        sort_users(sort_by)
    elif choice == 8:
        search_users()
    elif choice == 9:
        show_overdue_users()


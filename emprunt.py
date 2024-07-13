from datetime import datetime, timedelta
import json

def emprunter_livre():
    user_id = input("Entrez l'ID de l'utilisateur : ")
    book_title = input("Entrez le titre du livre à emprunter : ")
    borrow_date = datetime.now().strftime("%Y-%m-%d")
    return_date = (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d")  # Date de retour après 14 jours

    with open("users.json", "r") as f:
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
            
            with open("users.json", "w") as f:
                json.dump(users, f)
            
            print(f"Le livre '{book_title}' a été emprunté par {user['name']} jusqu'au {return_date}.")
            return

    print("Utilisateur non trouvé.")


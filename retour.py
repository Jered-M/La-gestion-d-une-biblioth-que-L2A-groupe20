import json
from datetime import datetime


def retourner_livre():
    user_id = input("Entrez l'ID de l'utilisateur : ")
    book_title = input("Entrez le titre du livre à retourner : ")

    with open("users.json", "r") as f:
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
                    with open("users.json", "w") as f:
                        json.dump(users, f)
                    print(f"Le livre '{book_title}' a été retourné par {user['name']}.")
                    return

    print("Livre ou utilisateur non trouvé.")

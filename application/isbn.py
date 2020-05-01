import requests as req
from flask_login import current_user
from application.models import Book

def get_book_by_isbn(isbn):
    isbn_code = isbn.replace("-", "")
    request_result = req.get("https://openlibrary.org/api/books",
                            params = {
                                "bibkeys": f"ISBN:{isbn_code}",
                                "format": "json",
                                "jscmd": "data"
                            })

    if request_result:
        request_data = request_result.json()

        if request_data == {}:
            return None

        title = request_data[f"ISBN:{isbn_code}"]["title"]
        image = request_data[f"ISBN:{isbn_code}"]["cover"]["large"]
        author = request_data[f"ISBN:{isbn_code}"]["authors"][0]["name"]

        book = Book(title=title, author=author, image=image,
                user_id=current_user.id)
        return book
    return None

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

        authors = "; "
        author_list = []
        for author in request_data[f"ISBN:{isbn_code}"]["authors"]:
            author_list.append(author["name"])
        authors = authors.join(author_list)

        book = Book(title=title, author=authors, image=image,
                user_id=current_user.id)
        return book
    return None

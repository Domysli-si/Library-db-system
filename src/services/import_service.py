import json
from src.repositories.author_repository import AuthorRepository
from src.repositories.book_repository import BookRepository
from src.repositories.category_repository import CategoryRepository
from src.repositories.book_category_repository import BookCategoryRepository
from src.db.connection import DatabaseConnection, DatabaseError
from datetime import datetime


class ImportService:
    """
    Import JSON data into multiple tables:
    - authors
    - books
    - categories + book_category (M:N)
    """

    def __init__(self, db_conn: DatabaseConnection):
        self.db_conn = db_conn

    def import_from_json(self, json_path: str):
        """
        JSON format example:
        [
            {
                "title": "Book Title",
                "author": "Author Name",
                "price": 12.5,
                "published_date": "2020-01-01",
                "categories": ["fiction", "study"]
            },
            ...
        ]
        """
        try:
            with open(json_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            raise DatabaseError(f"Failed to load JSON file: {e}")

        try:
            with self.db_conn.transaction() as conn:
                author_repo = AuthorRepository(conn)
                book_repo = BookRepository(conn)
                category_repo = CategoryRepository(conn)
                bc_repo = BookCategoryRepository(conn)

                for item in data:
                    # Add or get author
                    authors = [a for a in author_repo.get_all() if a.name == item["author"]]
                    if authors:
                        author_id = authors[0].id
                    else:
                        author_id = author_repo.add(type('Author', (), {'name': item["author"]})())

                    # Add book
                    published_date = datetime.strptime(item["published_date"], "%Y-%m-%d").date()
                    book_id = book_repo.add(type('Book', (), {
                        'title': item["title"],
                        'author_id': author_id,
                        'price': float(item["price"]),
                        'available': True,
                        'published_date': published_date
                    })())

                    # Add categories + M:N
                    for cat_name in item.get("categories", []):
                        cats = [c for c in category_repo.get_all() if c.name == cat_name]
                        if cats:
                            category_id = cats[0].id
                        else:
                            # Default type to 'fiction' if unknown
                            category_id = category_repo.add(type('Category', (), {
                                'name': cat_name,
                                'category_type': 'fiction'
                            })())
                        bc_repo.add(book_id, category_id)

        except Exception as e:
            raise DatabaseError(f"JSON import failed: {e}")


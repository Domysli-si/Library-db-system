import json
from datetime import datetime
from src.repositories.author_repository import AuthorRepository
from src.repositories.book_repository import BookRepository
from src.repositories.category_repository import CategoryRepository
from src.repositories.book_category_repository import BookCategoryRepository
from src.db.connection import DatabaseConnection, DatabaseError


class ImportService:
    def __init__(self, db_conn: DatabaseConnection):
        self.db_conn = db_conn

    def import_from_json(self, json_path: str):
        required_fields = ["title", "author", "price", "published_date", "categories"]

        try:
            with open(json_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            raise DatabaseError(f"Failed to load JSON file: {e}")

        for idx, item in enumerate(data, start=1):
            for field in required_fields:
                if field not in item:
                    raise ValueError(f"Item {idx} is missing required field '{field}'")

            if not isinstance(item["title"], str) or not item["title"].strip():
                raise ValueError(f"Item {idx} has invalid title")

            if not isinstance(item["author"], str) or not item["author"].strip():
                raise ValueError(f"Item {idx} has invalid author")

            try:
                item["price"] = float(item["price"])
            except (ValueError, TypeError):
                raise ValueError(f"Item {idx} has invalid price")

            try:
                datetime.strptime(item["published_date"], "%Y-%m-%d")
            except ValueError:
                raise ValueError(f"Item {idx} has invalid published_date format, expected YYYY-MM-DD")

            if not isinstance(item["categories"], list) or not all(isinstance(c, str) for c in item["categories"]):
                raise ValueError(f"Item {idx} has invalid categories list")

        try:
            with self.db_conn.transaction() as conn:
                author_repo = AuthorRepository(conn)
                book_repo = BookRepository(conn)
                category_repo = CategoryRepository(conn)
                bc_repo = BookCategoryRepository(conn)

                for item in data:
                    authors = [a for a in author_repo.get_all() if a.name == item["author"]]
                    if authors:
                        author_id = authors[0].id
                    else:
                        author_id = author_repo.add(type('Author', (), {'name': item["author"]})())

                    published_date = datetime.strptime(item["published_date"], "%Y-%m-%d").date()
                    book_id = book_repo.add(type('Book', (), {
                        'title': item["title"],
                        'author_id': author_id,
                        'price': item["price"],
                        'available': True,
                        'published_date': published_date
                    })())

                    for cat_name in item["categories"]:
                        cats = [c for c in category_repo.get_all() if c.name == cat_name]
                        if cats:
                            category_id = cats[0].id
                        else:
                            category_id = category_repo.add(type('Category', (), {
                                'name': cat_name,
                                'category_type': 'fiction'
                            })())
                        bc_repo.add(book_id, category_id)

        except Exception as e:
            raise DatabaseError(f"JSON import failed: {e}")


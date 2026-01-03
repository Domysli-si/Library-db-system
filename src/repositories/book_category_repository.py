from .base_repository import BaseRepository

class BookCategoryRepository(BaseRepository):
    def add(self, book_id: int, category_id: int):
        self.execute(
            "INSERT INTO book_category (book_id, category_id) VALUES (?, ?)",
            (book_id, category_id)
        )
        self.conn.commit()

    def remove(self, book_id: int, category_id: int):
        self.execute(
            "DELETE FROM book_category WHERE book_id=? AND category_id=?",
            (book_id, category_id)
        )
        self.conn.commit()

    def get_categories_for_book(self, book_id: int):
        cursor = self.execute(
            "SELECT category_id FROM book_category WHERE book_id=?",
            (book_id,)
        )
        return [row.category_id for row in cursor.fetchall()]

    def get_books_for_category(self, category_id: int):
        cursor = self.execute(
            "SELECT book_id FROM book_category WHERE category_id=?",
            (category_id,)
        )
        return [row.book_id for row in cursor.fetchall()]


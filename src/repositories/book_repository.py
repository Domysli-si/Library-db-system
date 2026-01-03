from .base_repository import BaseRepository
from src.models.book import Book

class BookRepository(BaseRepository):

    def add(self, book: Book) -> int:
        cursor = self.execute(
            """INSERT INTO book (title, author_id, price, available, published_date)
               OUTPUT INSERTED.id
               VALUES (?, ?, ?, ?, ?)""",
            (book.title, book.author_id, book.price, int(book.available), book.published_date)
        )
        new_id = cursor.fetchone()[0]
        self.conn.commit()
        return new_id

    def get_all(self):
        cursor = self.execute("SELECT id, title, author_id, price, available, published_date FROM book")
        return [
            Book(
                id=row.id,
                title=row.title,
                author_id=row.author_id,
                price=row.price,
                available=bool(row.available),
                published_date=row.published_date
            )
            for row in cursor.fetchall()
        ]

    def get_by_id(self, book_id: int):
        cursor = self.execute("SELECT id, title, author_id, price, available, published_date FROM book WHERE id = ?", (book_id,))
        row = cursor.fetchone()
        if row:
            return Book(
                id=row.id,
                title=row.title,
                author_id=row.author_id,
                price=row.price,
                available=bool(row.available),
                published_date=row.published_date
            )
        return None

    def update(self, book: Book):
        self.execute(
            """UPDATE book SET title=?, author_id=?, price=?, available=?, published_date=? WHERE id=?""",
            (book.title, book.author_id, book.price, int(book.available), book.published_date, book.id)
        )
        self.conn.commit()

    def delete(self, book_id: int):
        self.execute("DELETE FROM book WHERE id=?", (book_id,))
        self.conn.commit()


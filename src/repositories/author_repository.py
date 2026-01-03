from .base_repository import BaseRepository
from src.models.author import Author

class AuthorRepository(BaseRepository):

    def add(self, author: Author) -> int:
        """
        Insert new author and return new id
        """
        cursor = self.execute(
            "INSERT INTO author (name) OUTPUT INSERTED.id VALUES (?)",
            (author.name,)
        )
        new_id = cursor.fetchone()[0]
        self.conn.commit()
        return new_id

    def get_all(self):
        """
        Return list of all authors
        """
        cursor = self.execute("SELECT id, name FROM author")
        return [Author(id=row.id, name=row.name) for row in cursor.fetchall()]

    def get_by_id(self, author_id: int):
        cursor = self.execute("SELECT id, name FROM author WHERE id = ?", (author_id,))
        row = cursor.fetchone()
        if row:
            return Author(id=row.id, name=row.name)
        return None

    def update(self, author: Author):
        self.execute(
            "UPDATE author SET name = ? WHERE id = ?",
            (author.name, author.id)
        )
        self.conn.commit()

    def delete(self, author_id: int):
        self.execute("DELETE FROM author WHERE id = ?", (author_id,))
        self.conn.commit()


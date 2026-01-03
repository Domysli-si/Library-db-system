from .base_repository import BaseRepository
from src.models.library_user import LibraryUser

class UserRepository(BaseRepository):

    def add(self, user: LibraryUser) -> int:
        cursor = self.execute(
            """INSERT INTO library_user (full_name, email, active, created_at)
               OUTPUT INSERTED.id
               VALUES (?, ?, ?, ?)""",
            (user.full_name, user.email, int(user.active), user.created_at)
        )
        new_id = cursor.fetchone()[0]
        self.conn.commit()
        return new_id

    def get_all(self):
        cursor = self.execute("SELECT id, full_name, email, active, created_at FROM library_user")
        return [
            LibraryUser(
                id=row.id,
                full_name=row.full_name,
                email=row.email,
                active=bool(row.active),
                created_at=row.created_at
            ) for row in cursor.fetchall()
        ]

    def get_by_id(self, user_id: int):
        cursor = self.execute("SELECT id, full_name, email, active, created_at FROM library_user WHERE id=?", (user_id,))
        row = cursor.fetchone()
        if row:
            return LibraryUser(
                id=row.id,
                full_name=row.full_name,
                email=row.email,
                active=bool(row.active),
                created_at=row.created_at
            )
        return None

    def update(self, user: LibraryUser):
        self.execute(
            "UPDATE library_user SET full_name=?, email=?, active=? WHERE id=?",
            (user.full_name, user.email, int(user.active), user.id)
        )
        self.conn.commit()

    def delete(self, user_id: int):
        self.execute("DELETE FROM library_user WHERE id=?", (user_id,))
        self.conn.commit()


from .base_repository import BaseRepository
from src.models.category import Category

class CategoryRepository(BaseRepository):

    def add(self, category: Category) -> int:
        cursor = self.execute(
            "INSERT INTO category (name, category_type) OUTPUT INSERTED.id VALUES (?, ?)",
            (category.name, category.category_type)
        )
        new_id = cursor.fetchone()[0]
        self.conn.commit()
        return new_id

    def get_all(self):
        cursor = self.execute("SELECT id, name, category_type FROM category")
        return [Category(id=row.id, name=row.name, category_type=row.category_type) for row in cursor.fetchall()]

    def get_by_id(self, category_id: int):
        cursor = self.execute("SELECT id, name, category_type FROM category WHERE id=?", (category_id,))
        row = cursor.fetchone()
        if row:
            return Category(id=row.id, name=row.name, category_type=row.category_type)
        return None

    def update(self, category: Category):
        self.execute(
            "UPDATE category SET name=?, category_type=? WHERE id=?",
            (category.name, category.category_type, category.id)
        )
        self.conn.commit()

    def delete(self, category_id: int):
        self.execute("DELETE FROM category WHERE id=?", (category_id,))
        self.conn.commit()


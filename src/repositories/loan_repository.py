from .base_repository import BaseRepository
from src.models.loan import Loan

class LoanRepository(BaseRepository):

    def add(self, loan: Loan) -> int:
        cursor = self.execute(
            """INSERT INTO loan (book_id, user_id, loan_date, return_date, returned)
               OUTPUT INSERTED.id
               VALUES (?, ?, ?, ?, ?)""",
            (loan.book_id, loan.user_id, loan.loan_date, loan.return_date, int(loan.returned))
        )
        new_id = cursor.fetchone()[0]
        self.conn.commit()
        return new_id

    def get_all(self):
        cursor = self.execute("SELECT id, book_id, user_id, loan_date, return_date, returned FROM loan")
        return [
            Loan(
                id=row.id,
                book_id=row.book_id,
                user_id=row.user_id,
                loan_date=row.loan_date,
                return_date=row.return_date,
                returned=bool(row.returned)
            ) for row in cursor.fetchall()
        ]

    def update(self, loan: Loan):
        self.execute(
            "UPDATE loan SET book_id=?, user_id=?, loan_date=?, return_date=?, returned=? WHERE id=?",
            (loan.book_id, loan.user_id, loan.loan_date, loan.return_date, int(loan.returned), loan.id)
        )
        self.conn.commit()

    def delete(self, loan_id: int):
        self.execute("DELETE FROM loan WHERE id=?", (loan_id,))
        self.conn.commit()


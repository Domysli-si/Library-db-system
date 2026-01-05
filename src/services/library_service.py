from src.repositories.book_repository import BookRepository
from src.repositories.user_repository import UserRepository
from src.repositories.loan_repository import LoanRepository
from src.repositories.author_repository import AuthorRepository
from src.repositories.book_category_repository import BookCategoryRepository
from src.repositories.category_repository import CategoryRepository
from src.db.connection import DatabaseConnection, DatabaseError
from src.models.loan import Loan
from datetime import datetime


class LibraryService:
    """
    Service layer handling business logic:
    - loan/return books (transactional)
    - JSON import (authors, books, categories)
    """

    def __init__(self, db_conn: DatabaseConnection):
        self.db_conn = db_conn

    def loan_book(self, book_id: int, user_id: int) -> Loan:
        """
        Loan a book to a user. Transactional: Book availability + Loan record
        """
        try:
            with self.db_conn.transaction() as conn:
                book_repo = BookRepository(conn)
                loan_repo = LoanRepository(conn)

                # Get the book
                book = book_repo.get_by_id(book_id)
                if not book:
                    raise ValueError("Book not found")
                if not book.available:
                    raise ValueError("Book is currently not available")

                # Mark book as unavailable
                book.available = False
                book_repo.update(book)

                # Create loan record
                loan = Loan(
                    book_id=book_id,
                    user_id=user_id,
                    loan_date=datetime.now(),
                    return_date=None,
                    returned=False
                )
                loan_repo.add(loan)

                return loan

        except Exception as e:
            raise DatabaseError(f"Loan transaction failed: {e}")

    def return_book(self, loan_id: int):
        """
        Return a book: sets loan returned flag + book availability
        """
        try:
            with self.db_conn.transaction() as conn:
                loan_repo = LoanRepository(conn)
                book_repo = BookRepository(conn)

                # Get the loan
                loans = loan_repo.get_all()
                loan = next((l for l in loans if l.id == loan_id), None)
                if not loan:
                    raise ValueError("Loan not found")
                if loan.returned:
                    raise ValueError("Book already returned")

                # Update loan record
                loan.returned = True
                loan.return_date = datetime.now()
                loan_repo.update(loan)

                # Update book availability
                book = book_repo.get_by_id(loan.book_id)
                if book:
                    book.available = True
                    book_repo.update(book)

        except Exception as e:
            raise DatabaseError(f"Return transaction failed: {e}")


# Loan entity
class Loan:
    def __init__(self, id: int = None, book_id: int = None, user_id: int = None,
                 loan_date=None, return_date=None, returned: bool = False):
        self.id = id
        self.book_id = book_id
        self.user_id = user_id
        self.loan_date = loan_date
        self.return_date = return_date
        self.returned = returned


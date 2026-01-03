# Book entity
class Book:
    def __init__(self, id: int = None, title: str = "", author_id: int = None,
                 price: float = 0.0, available: bool = True, published_date=None):
        self.id = id
        self.title = title
        self.author_id = author_id
        self.price = price
        self.available = available
        self.published_date = published_date


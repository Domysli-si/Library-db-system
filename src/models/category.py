# Category entity
class Category:
    def __init__(self, id: int = None, name: str = "", category_type: str = ""):
        self.id = id
        self.name = name
        self.category_type = category_type  # must match ENUM: fiction, nonfiction, study


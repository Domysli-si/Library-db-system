# Library user entity
class LibraryUser:
    def __init__(self, id: int = None, full_name: str = "", email: str = "",
                 active: bool = True, created_at=None):
        self.id = id
        self.full_name = full_name
        self.email = email
        self.active = active
        self.created_at = created_at


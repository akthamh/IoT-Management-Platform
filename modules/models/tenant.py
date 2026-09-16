class Tenant:
    def __init__(
        self,
        id: int | None,
        name: str,
        address: str | None,
        is_active: bool,
        created_at: str | None
     ):

        self.id = id
        self.name = name
        self.address = address
        self.is_active = is_active
        self.created_at = created_at
class Device:
    def __init__(
        self,
        id: int | None,
        name: str,
        category: str,
        device_type: str,
        manufacturer: str | None,
        model: str | None,
        serial_number: str | None,
        location: str | None,
        status: str,
        tenant_id: int
    ):
        self.id = id
        self.name = name
        self.category = category
        self.device_type = device_type
        self.manufacturer = manufacturer
        self.model = model
        self.serial_number = serial_number
        self.location = location
        self.status = status
        self.tenant_id = tenant_id
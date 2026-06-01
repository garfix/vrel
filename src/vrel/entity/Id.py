class Id:

    id: str
    type: str

    def __init__(self, id: str, type: str):
        self.id = id
        self.type = type

    def __repr__(self) -> str:
        return f"`{self.type}:{self.id}`"

    def __eq__(self, value):
        return isinstance(value, Id) and self.id == value.id and self.type == value.type

    def __hash__(self) -> int:
        return hash((self.id, self.type))

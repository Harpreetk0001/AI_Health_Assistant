from sqlalchemy.ext.declarative import as_declarative, declared_attr
@as_declarative()
class Base:
    id: any
    __name__: str
    @declared_attr
    def __tablename__(cls) -> str:
        # This will set the table name automatically as the lower-case class name
        return cls.__name__.lower()

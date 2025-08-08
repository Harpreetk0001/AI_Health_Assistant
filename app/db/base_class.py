from sqlalchemy.ext.declarative import as_declarative, declared_attr # Import decorators to help define base class for SQLAlchemy models
@as_declarative() # Mark this class as the base for all database models
class Base:
    id: any # Every model will have an 'id' attribute (type can be anything)
    __name__: str # The name of the class as a string
    @declared_attr  # This special method runs once per model class to set the table name
    def __tablename__(cls) -> str:
        # This will set the table name automatically as the lower-case class name
        return cls.__name__.lower() # Automatically make the database table name the lowercase of the model class name

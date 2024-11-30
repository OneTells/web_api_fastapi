from sqlalchemy import Integer, Text, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped


class Base(DeclarativeBase):
    pass


class Product(Base):
    __tablename__ = "products"

    id: Mapped[str] = mapped_column(Integer, primary_key=True, autoincrement=True)

    slug: Mapped[str] = mapped_column(Text, nullable=False)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    price: Mapped[int] = mapped_column(Integer, nullable=False)

    # noinspection PyTypeChecker
    __table_args__ = (
        UniqueConstraint(slug, name='products_uc'),
    )

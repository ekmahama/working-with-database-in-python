from sqlalchemy import String, Numeric, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass

class Investment(Base):
    __tablename__= "investment"
    id:Mapped[int] = mapped_column(primary_key=True)
    coin: Mapped[str] = mapped_column(String(32))
    currency: Mapped[str] = mapped_column(String(3))
    amount: Mapped[float] = mapped_column(Numeric(5,2))

    def __str__(self):
        return f"<Investment coin: :{self.coin}, currency: {self.currency}, amount: {self.amount}>"
    

engine = create_engine("sqlite:///demo.db")
Base.metadata.create_all(engine)
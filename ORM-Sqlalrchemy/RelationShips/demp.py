from sqlalchemy import String, Numeric, create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session


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
    

engine = create_engine("sqlite:///demo_r.db")
Base.metadata.create_all(engine)


bitcoin = Investment(coin="bitcoin", currency='usd', amount = 1.0)
ethereum = Investment(coin="ethereum", currency='gpb', amount = 2.0)
solana = Investment(coin="solana", currency='usd', amount = 10.0)


with Session(engine) as session:
    pass




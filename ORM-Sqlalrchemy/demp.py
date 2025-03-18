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
    

engine = create_engine("sqlite:///demo.db")
Base.metadata.create_all(engine)


bitcoin = Investment(coin="bitcoin", currency='usd', amount = 1.0)
ethereum = Investment(coin="ethereum", currency='gpb', amount = 2.0)
solana = Investment(coin="solana", currency='usd', amount = 10.0)


with Session(engine) as session:
    # session.add(bitcoin)
    # session.add_all([ethereum, solana])

    # session.commit()

    # this will throw exception if "bitcoin" does not exist
    stmt = select(Investment).where(Investment.coin == "bitcoin")
    print(stmt)
    investment = session.execute(stmt).scalar_one()
    print(investment)

    # retrieve with primay key
    # this will return None if primary key does not exist
    ethereum = session.get(Investment, 2)
    print(solana)

    # Get all
    # This will return None for empty list
    stmt = select(Investment).where(Investment.amount > 1)
    all_investments = session.execute(stmt).scalars().all()
    # for invest in all_investments:
    #     print(invest)

    # Update 
    bitcoin = session.get(Investment, 1)
    bitcoin.amount = 5.5
    print(session.dirty)
    session.commit()
    print(bitcoin)

    # Delete
    solana = session.get(Investment,2)
    session.delete(solana)
    print(session.deleted)
    session.commit()



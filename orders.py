import json

from sqlalchemy import select
from sqlalchemy.orm import sessionmaker, Session

import db_types
from db_types import Orders

def create_order_row(engine, items: list[int], user_id: int, status: str) -> int:
    new_order = Orders(
        list_of_unique_ids=json.dumps(items),
        user_id=user_id,
        status=status
    )

    # Ensure your Orders.id is declared like:
    # id = mapped_column(Integer, primary_key=True, autoincrement=True)

    with Session(engine) as session:
        session.add(new_order)
        session.flush()          # PK is assigned here
        new_id = new_order.id    # grab it before commit if you want
        session.commit()
        return new_id


def get_order_object(engine, order_id: int):
    with Session(engine) as session:
        found_order = session.get(Orders, order_id)
        return found_order

def get_user_orders(engine, user: db_types.Users):
    with Session(engine) as session:
        user_id = user.id

        stmt = select(Orders).where(Orders.user_id == user_id)
        values = session.execute(stmt).scalars().all()

        return values
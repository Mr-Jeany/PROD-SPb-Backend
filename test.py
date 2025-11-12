from sqlalchemy import create_engine, text
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(
    "postgresql+psycopg2://admin:admin@0.0.0.0:5432/maindatabase"
)

db = scoped_session(sessionmaker(bind=engine))

# Example query
result = db.execute(text("SELECT * FROM my_table")).fetchall()
for row in result:
    print(row)

from sqlalchemy import text
from db.connection import SessionLocal

session = SessionLocal()

result = session.execute(text("SELECT 1"))
print(result.fetchone())

session.close()

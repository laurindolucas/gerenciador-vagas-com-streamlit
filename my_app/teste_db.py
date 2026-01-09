from db.connection import SessionLocal

session = SessionLocal()
result = session.execute("SELECT 1")
print(result.fetchone())
session.close()

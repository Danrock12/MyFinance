from app.db import Base, engine
from app.models import Account

Base.metadata.create_all(bind=engine)
print("Tables created successfully")

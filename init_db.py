from database import engine, Base
from models import Users, Products, Orders, Notifications


Base.metadata.create_all(bind=engine)

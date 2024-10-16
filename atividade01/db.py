from sqlmodel import SQLModel, create_engine, Session

sqlite_url = "sqlite:///database.db"
engine = create_engine(sqlite_url, echo=True)

def init_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    return Session(engine)

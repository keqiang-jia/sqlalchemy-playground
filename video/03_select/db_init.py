import sqlalchemy

engine = sqlalchemy.create_engine('mysql+pymysql://root:123456@172.29.44.161:3306/test?charset=utf8', echo=True)

meta_data = sqlalchemy.MetaData()

person_table = sqlalchemy.Table(
    "person", meta_data,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String(128), unique=True, nullable=False),
    sqlalchemy.Column("birthday", sqlalchemy.Date, nullable=False),
)

meta_data.create_all(engine)

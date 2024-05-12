import sqlalchemy


engine = sqlalchemy.create_engine('mysql+pymysql://root:123456@172.29.44.161:3306/test?charset=utf8')
conn = engine.connect()

query = sqlalchemy.text('SELECT * FROM students')
result_set = conn.execute(query)

for row in result_set:
    print(row)

conn.close()

engine.dispose()

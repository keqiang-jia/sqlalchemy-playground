# flask_sqlalchemy playground

- demo1：使用flask_sqlalchemy进行各种数据库操作
- demo2：使用flask_sqlalchemy进行多对多关系的操作
- demo3：sqlalchemy的demo1版本
- demo4：sqlalchemy的demo2版本

**flask-sqlalchemy 和 sqlalchemy的区别**

```
diff demo1 demo3
diff demo2 demo4
diff demo1_test.py demo3_test.py
diff demo2_test.py demo4_test.py
```

**flask-sqlalchemy支持迁移**
```
flask --app demo1 db init
flask --app demo1 db migrate
flask --app demo1 db upgrade
```

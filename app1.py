from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import unittest
from sqlalchemy import text

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@172.29.44.161:3306/test?charset=utf8'

db = SQLAlchemy(app)
migrate = Migrate(app, db)


# with app.app_context():
#     with db.engine.connect() as conn:
#         rs = conn.execute(text("SELECT 1"))
#         print(rs.fetchone())

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100))
    password = db.Column(db.String(100))

    extension = db.relationship("UserExtension", back_populates="user", uselist=False)

    # articles = db.relationship("Article")


class UserExtension(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    school = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), unique=True)
    user = db.relationship("User", back_populates="extension")


article_tag_table = db.Table(
    "article_tag_table",
    db.Column("article_id", db.Integer, db.ForeignKey(
        "article.id"), primary_key=True),
    db.Column("tag_id", db.Integer, db.ForeignKey("tag.id"), primary_key=True)
)


class Article(db.Model):
    __tablename__ = "article"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)

    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    author = db.relationship("User", backref="articles")

    tags = db.relationship("Tag", secondary=article_tag_table, back_populates="articles")


class Tag(db.Model):
    __tablename__ = "tag"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))

    articles = db.relationship("Article", secondary=article_tag_table, back_populates="tags")


class Category(db.Model):
    __tablename__ = "category"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))
    newses = db.relationship("News", back_populates="category", cascade="merge")


class News(db.Model):
    __tablename__ = "news"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100))
    content = db.Column(db.Text)
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"))
    category = db.relationship("Category", back_populates="newses", cascade="expunge")


@app.cli.command()
def create():
    db.drop_all()
    db.create_all()


class TestHelloFunction(unittest.TestCase):
    def setUp(self):
        app.app_context().push()

    def test_user_add(self):
        user1 = User(username="张三", password="444444")
        user2 = User(username="李四", password="555555")
        user3 = User(username="王五", password="666666")
        db.session.add(user1)
        db.session.add(user2)
        db.session.add(user3)
        db.session.commit()
        return "用户添加成功！"

    def test_user_fetch(self):
        print("获取所有用户数据：")
        users = User.query.all()
        for user in users:
            print(user.username)

        print("获取主键为1的User对象：")
        user = db.session.get(User, 1)
        print(user.username)

        print("获取第一条数据：")
        user = User.query.first()
        print(user.username)

    def test_user_filter(self):
        print("使用filter方法获取用户名为张三的用户数据：")
        users = User.query.filter(User.username == "张三").all()
        print(users)

        print("使用filter_by方法获取用户名为张三的用户数据：")
        users = User.query.filter_by(username="张三").all()
        print(users)

        print("按照id排序：")
        users = User.query.order_by("id").all()
        print(users)
        users = User.query.order_by(User.id).all()
        print(users)

        print("按照id倒序排序：")
        from sqlalchemy import desc
        users = User.query.order_by(db.text("-id")).all()
        print(users)
        users = User.query.order_by(User.id.desc()).all()
        print(users)

        users = User.query.order_by(desc("id")).all()
        print(users)

        print("按照用户名分组：")
        from sqlalchemy import func
        users = db.session.query(User.username, func.count(
            User.id)).group_by("username").all()
        print(users)

        print("contains和like方法：")
        users = User.query.filter(User.username.contains("张")).all()
        print(users)
        users = User.query.filter(User.username.like("%张%")).all()
        print(users)

        print("in_和not_in方法：")
        users = User.query.filter(User.username.in_(["张三", "李四", "王五"])).all()
        print(users)
        users = User.query.filter(~User.username.in_(['张三'])).all()
        print(users)

        print("is null和is not null方法：")
        users = User.query.filter(User.username == None).all()
        print(users)
        users = User.query.filter(User.username.is_(None)).all()
        print(users)

        users = User.query.filter(User.username != None).all()
        print(users)
        users = User.query.filter(User.username.isnot(None)).all()
        print(users)

        print("and_和or_方法：")
        from sqlalchemy import and_
        users = User.query.filter(and_(User.username == "张三", User.id < 10)).all()
        print(users)

        from sqlalchemy import or_
        users = User.query.filter(or_(User.username == "张三", User.username == "李四")).all()
        print(users)

    def test_user_update(self):
        # 1. 修改一条数据
        user = User.query.get(1)
        user.username = "张三_重新修改的"
        db.session.commit()

        # 2. 批量修改数据
        User.query.filter(User.username.like("%张三%")).update(
            {"password": User.password + "_被修改的"})
        db.session.commit()
        return "数据修改成功！"

    def test_user_delete(self):
        # user = User.query.get(1)
        # db.session.delete(user)
        # db.session.commit()

        # User.query.filter(User.username.contains("张三")).delete(synchronize_session=False)
        # db.session.commit()

        users = User.query.filter(User.username.contains("张三"))
        print(type(users))

        return "数据删除成功"

    def test_article_add(self):
        user = User.query.first()
        article = Article(title="aa", content="bb", author=user)
        db.session.add(article)
        db.session.commit()

        article = Article.query.filter_by(title="aa").first()
        print("relationship的功能")
        print(article.author.username)

    def test_user_visit_articles(self):
        print("relationship+backref的功能")
        user = User.query.first()
        for article in user.articles:
            print(article.title)

    def test_one2one(self):
        user = User.query.first()
        extension1 = UserExtension(school="清华大学", user=user)
        # extension2 = UserExtension(school="北京大学",user=user)
        db.session.add(extension1)
        # db.session.add(extension2)
        db.session.commit()

    def test_many2many(self):
        article1 = Article(title="11", content="aa")
        article2 = Article(title="22", content="bb")

        tag1 = Tag(name="python")
        tag2 = Tag(name="flask")

        article1.tags.append(tag1)
        article1.tags.append(tag2)

        article2.tags.append(tag1)
        article2.tags.append(tag2)

        db.session.add_all([article1, article2])
        db.session.commit()

    def test_save_update(self):
        category = Category(name="军事")
        news = News(title="新闻1", content="新闻内容1")
        news.category = category
        db.session.add(category)
        db.session.commit()

    def test_delete_view(self):
        news = News.query.first()
        db.session.delete(news)
        db.session.commit()

    def test_delete_orphan_view(self):
        category = Category.query.first()
        news = News(title="新闻2", content="新闻内容2")
        category.newses.append(news)
        db.session.commit()

        # 将news从category中解除关联
        category.newses.remove(news)
        db.session.commit()

    def test_merge_view(self):
        news1 = News.query.first()

        category = Category(name="分类2")
        news2 = News(title="标题2", category=category)

        # 将news2.id设置为news1.id，在merge的时候就会根据news2的id去寻找需要merge的对象
        # 这里需要merge的就是news1，然后将news2上和news1上不同的数据复制到news1上
        news2.id = news1.id
        db.session.merge(news2)
        db.session.commit()

    def test_expunge_view(self):
        news = News.query.first()
        category = news.category

        db.session.expunge(news)
        category.name = '测试分类'
        db.session.commit()


if __name__ == '__main__':
    unittest.main()

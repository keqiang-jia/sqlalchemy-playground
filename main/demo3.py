from sqlalchemy import Column, Integer, String, ForeignKey, create_engine, Text
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(100))
    password = Column(String(100))

    extension = relationship("UserExtension", back_populates="user", uselist=False)

    # articles = relationship("Article")


class UserExtension(Base):
    __tablename__ = "user_extension"
    id = Column(Integer, primary_key=True, autoincrement=True)
    school = Column(String(100))

    user_id = Column(Integer, ForeignKey("user.id"), unique=True)
    user = relationship("User", back_populates="extension")


class ArticleTagTable(Base):
    __tablename__ = "article_tag_table"
    id = Column(Integer, primary_key=True, autoincrement=True)
    article_id = Column(Integer, ForeignKey("article.id"))
    tag_id = Column(Integer, ForeignKey("tag.id"))


class Article(Base):
    __tablename__ = "article"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)

    author_id = Column(Integer, ForeignKey("user.id"))
    author = relationship("User", backref="articles")

    tags = relationship("Tag", secondary='article_tag_table', back_populates="articles")


class Tag(Base):
    __tablename__ = "tag"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100))

    articles = relationship("Article", secondary='article_tag_table', back_populates="tags")


class Category(Base):
    __tablename__ = "category"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100))
    newses = relationship("News", back_populates="category", cascade="merge")


class News(Base):
    __tablename__ = "news"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(100))
    content = Column(Text)
    category_id = Column(Integer, ForeignKey("category.id"))
    category = relationship("Category", back_populates="newses", cascade="expunge")


if __name__ == '__main__':
    engine = create_engine("mysql+pymysql://root:123456@172.29.44.161:3306/test?charset=utf8")
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

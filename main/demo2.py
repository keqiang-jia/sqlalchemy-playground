from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@172.29.44.161:3306/test?charset=utf8'
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120))
    password = db.Column(db.String(128))

    roles = db.relationship('Role', secondary="user_role", back_populates='users', lazy='dynamic')


user_role = db.Table(
    "user_role",
    db.Column("id", db.Integer, primary_key=True, autoincrement=True),
    db.Column("user_id", db.Integer, db.ForeignKey("user.id")),
    db.Column("role_id", db.Integer, db.ForeignKey("role.id")),
)


class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    code = db.Column(db.String(64), unique=True)

    users = db.relationship('User', secondary="user_role", back_populates='roles', lazy='dynamic')
    permissions = db.relationship('Permission', secondary="role_permission", back_populates='roles', lazy='dynamic')


role_permission = db.Table(
    "role_permission",
    db.Column("id", db.Integer, primary_key=True, autoincrement=True),
    db.Column("permission_id", db.Integer, db.ForeignKey("permission.id")),
    db.Column("role_id", db.Integer, db.ForeignKey("role.id")),
)


class Permission(db.Model):
    __tablename__ = 'permission'
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(64), unique=True)
    code = db.Column(db.String(64))

    roles = db.relationship('Role', secondary="role_permission", back_populates='permissions', lazy='dynamic')

    parent_id = db.Column(db.Integer, db.ForeignKey("permission.id"))
    parent = db.relationship("Permission", remote_side=[id])  # 自关联


if __name__ == '__main__':
    with app.app_context():
        db.drop_all()
        db.create_all()

        # 权限表填充数据
        permission1 = Permission(url='/auth/read', code='read')
        permission2 = Permission(url='/auth/comment', code='comment')
        permission3 = Permission(url='/auth/write', code='write')
        permission4 = Permission(url='/admin', code='admin')
        db.session.add(permission1)
        db.session.add(permission2)
        db.session.add(permission3)
        db.session.add(permission4)

        # 角色表填充数据
        role1 = Role(name='普通用户', code='level1')
        role2 = Role(name='会员用户', code='level2')
        role3 = Role(name='管理员用户', code='level3')
        db.session.add(role1)
        db.session.add(role2)
        db.session.add(role3)

        # 角色权限关联表填充数据
        role1.permissions.append(permission1)
        role1.permissions.append(permission2)

        role2.permissions.append(permission1)
        role2.permissions.append(permission2)
        role2.permissions.append(permission3)

        role3.permissions.append(permission1)
        role3.permissions.append(permission2)
        role3.permissions.append(permission3)
        role3.permissions.append(permission4)

        # 用户表填充数据
        user1 = User(username='张三', email='zhangsan@163.com', password='111111')
        user2 = User(username='李四', email='lisi@163.com', password='222222')
        user3 = User(username='王五', email='wangwu@163.com', password='333333')
        db.session.add(user1)
        db.session.add(user2)
        db.session.add(user3)

        # 用户角色关联表填充数据
        user1.roles.append(role1)
        user2.roles.append(role2)
        user3.roles.append(role3)

        db.session.commit()

from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, create_engine
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

Base = declarative_base()


class UserTable(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(80), nullable=False)
    email = Column(String(120))

    roles = relationship('RoleTable', secondary="user_role", back_populates='users', lazy='dynamic', passive_deletes=True)


class UserRoleTable(Base):
    __tablename__ = 'user_role'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.id", ondelete='CASCADE'))
    role_id = Column(Integer, ForeignKey("role.id", ondelete='CASCADE'))


class RoleTable(Base):
    __tablename__ = 'role'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(64), unique=True)
    modify_time = Column(DateTime, default=datetime.utcnow)

    users = relationship('UserTable', secondary="user_role", back_populates='roles', lazy='dynamic', passive_deletes=True)
    permissions = relationship('PermissionTable', secondary="role_permission", back_populates='roles', lazy='dynamic', passive_deletes=True)


class RolePermissionTable(Base):
    __tablename__ = 'role_permission'
    id = Column(Integer, primary_key=True, autoincrement=True)

    permission_id = Column(Integer, ForeignKey("permission.id", ondelete='CASCADE'))
    role_id = Column(Integer, ForeignKey("role.id", ondelete='CASCADE'))


class PermissionTable(Base):
    __tablename__ = 'permission'
    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String(64), unique=True)
    code = Column(String(64))

    parent_id = Column(Integer, ForeignKey("permission.id", ondelete='CASCADE'))
    roles = relationship('RoleTable', secondary="role_permission", back_populates='permissions', lazy='dynamic', passive_deletes=True)


if __name__ == '__main__':
    engine = create_engine("mysql+pymysql://root:123456@172.29.44.161:3306/test?charset=utf8")
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    Session = sessionmaker(engine)
    db_session = Session()

    # 权限表填充数据
    permission1 = PermissionTable(url='/auth/read', code='read')
    permission2 = PermissionTable(url='/auth/comment', code='comment')
    permission3 = PermissionTable(url='/auth/write', code='write')
    permission4 = PermissionTable(url='/admin', code='admin')
    db_session.add(permission1)
    db_session.add(permission2)
    db_session.add(permission3)
    db_session.add(permission4)

    # 角色表填充数据
    role1 = RoleTable(name='普通用户')
    role2 = RoleTable(name='会员用户')
    role3 = RoleTable(name='管理员用户')
    db_session.add(role1)
    db_session.add(role2)
    db_session.add(role3)

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
    user1 = UserTable(username='张三', email='zhangsan@163.com')
    user2 = UserTable(username='李四', email='lisi@163.com')
    user3 = UserTable(username='王五', email='wangwu@163.com')
    db_session.add(user1)
    db_session.add(user2)
    db_session.add(user3)

    # 用户角色关联表填充数据
    user1.roles.append(role1)
    user2.roles.append(role2)
    user3.roles.append(role3)

    db_session.commit()

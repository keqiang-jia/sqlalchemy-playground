import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main.demo4 import UserTable, RoleTable, PermissionTable

engine = create_engine("mysql+pymysql://root:123456@172.29.44.161:3306/test?charset=utf8")
Session = sessionmaker(engine)
db_session = Session()


class TestHelloFunction(unittest.TestCase):
    def setUp(self):
        pass

    def test_user_roles(self):
        user = db_session.get(UserTable, 1)
        print(user.username, user.email)

        for role in user.roles:
            print(role.name)

    def test_role_users(self):
        role = db_session.get(RoleTable, 1)
        print(role.name)

        for user in role.users:
            print(user.username, user.email)

    def test_role_permissions(self):
        role = db_session.get(RoleTable, 1)
        print(role.name)

        for permission in role.permissions:
            print(permission.url, permission.code)

    def test_permission_roles(self):
        permission = db_session.get(PermissionTable, 1)
        print(permission.url, permission.code)

        for role in permission.roles:
            print(role.name)

    def test_user_permissions(self):
        user = db_session.get(UserTable, 1)
        print(user.username, user.email)
        for role in user.roles:
            for permission in role.permissions:
                print(permission.url, permission.code)

    def tearDown(self):
        pass

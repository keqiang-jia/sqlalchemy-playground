import unittest

from main.demo2 import app, db, User, Role, Permission


class TestHelloFunction(unittest.TestCase):
    def setUp(self):
        app.app_context().push()

    def test_user_roles(self):
        user = db.session.get(User, 1)
        print(user.username, user.email, user.password)

        for role in user.roles:
            print(role.name, role.code)

    def test_role_users(self):
        role = db.session.get(Role, 1)
        print(role.name, role.code)

        for user in role.users:
            print(user.username, user.email, user.password)

    def test_role_permissions(self):
        role = db.session.get(Role, 1)
        print(role.name, role.code)

        for permission in role.permissions:
            print(permission.url, permission.code)

    def test_permission_roles(self):
        permission = db.session.get(Permission, 1)
        print(permission.url, permission.code)

        for role in permission.roles:
            print(role.name, role.code)

    def test_user_permissions(self):
        user = db.session.get(User, 1)
        print(user.username, user.email, user.password)
        for role in user.roles:
            for permission in role.permissions:
                print(permission.url, permission.code)

    def tearDown(self):
        # app.app_context().pop()
        pass
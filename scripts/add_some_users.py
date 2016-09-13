#!/usr/bin/env python
# coding: utf-8
import os
import sys


sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


if __name__ == '__main__':
    from builder.main import create_app
    app = create_app()

    with app.app_context():
        from builder.models import User, Role, UserRole

        print('Add users for system...')
        superuser = User.create(username='superuser',
                                email='superuser@prodam.sp.gov.br',
                                password='prodam123',
                                confirm_password='prodam123')

        commonuser = User.create(username='prodam',
                                 email='prodam@prodam.sp.gov.br',
                                 password='prodam123',
                                 confirm_password='prodam123')

        print('Add roles...')
        superuser_role = Role.create('superuser')
        admin_role = Role.create('admin')
        client_role = Role.create('client')
        reviewer_role = Role.create('reviewer')

        print('Set roles to user...')
        superuser.set_role(superuser_role)
        superuser.set_role(admin_role)
        superuser.set_role(client_role)
        superuser.set_role(reviewer_role)
        commonuser.set_role(reviewer_role)

        print('Finish!')
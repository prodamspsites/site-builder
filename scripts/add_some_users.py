#!/usr/bin/env python
# coding: utf-8
import os
import sys


sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


if __name__ == '__main__':
    from builder.main import create_app
    app = create_app()

    with app.app_context():
        from builder.models import User, Role

        print('Add users for system...')
        super_user = User.create(username='superuser',
                                 email='superuser@prodam.sp.gov.br',
                                 name='Prodam Superusuário',
                                 password='prodam123',
                                 confirm_password='prodam123')

        admin_user = User.create(username='admin',
                                 email='admin@prodam.sp.gov.br',
                                 name='Prodam Administrador',
                                 password='prodam123',
                                 confirm_password='prodam123')

        client_user = User.create(username='client',
                                  email='client@prodam.sp.gov.br',
                                  name='Prodam Cliente',
                                  password='prodam123',
                                  confirm_password='prodam123')

        common_user = User.create(username='prodam',
                                  email='prodam@prodam.sp.gov.br',
                                  name='Prodam Usuário Comum',
                                  password='prodam123',
                                  confirm_password='prodam123')

        print('Add roles...')
        superuser_role = Role.create(name='superuser', description='Super Usuário')
        admin_role = Role.create(name='admin', description='Administrador')
        client_role = Role.create(name='client', description='Cliente')

        print('Set roles to users...')
        super_user.set_role(superuser_role)
        admin_user.set_role(admin_role)
        client_user.set_role(client_role)

        print('Finish!')
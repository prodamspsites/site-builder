# coding: utf-8

if __name__ == '__main__':
    from builder.models import User, Role, UserRole

    superuser = User.create(username='superuser', email='superuser@prodam.sp.gov.br',
                            password='prodam123', confirm_password='prodam123')

    commonuser = User.create(username='prodam', email='prodam@prodam.sp.gov.br',
                             password='prodam123', confirm_password='prodam123')

    superuser_role = Role.create('superuser')
    admin_role = Role.create('admin')
    client_role = Role.create('client')
    reviewer_role = Role.create('reviewer')

    superuser.set_role(superuser_role)
    commonuser.set_role(reviewer_role)
# coding: utf-8
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from builder.main import create_app, db

app = create_app()
manager = Manager(app)
migrate = Migrate(app=app, db=db)

manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()

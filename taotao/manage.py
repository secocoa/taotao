
from flask_migrate import MigrateCommand
from flask_script import Manager
from app import create_app

app = create_app('developConfig')

manage = Manager(app)
manage.add_command('db',MigrateCommand)
if __name__ == '__main__':
    manage.run()
